from __future__ import annotations

import datetime as dt
import enum
from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence
from collections.abc import Set as AbstractSet
from contextlib import suppress
from dataclasses import asdict, dataclass
from datetime import timezone
from functools import partial, reduce
from itertools import chain
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    Literal,
    TypeAlias,
    TypeGuard,
    TypeVar,
    assert_never,
    cast,
    overload,
)
from uuid import UUID
from zoneinfo import ZoneInfo

import polars as pl
from polars import (
    Boolean,
    DataFrame,
    Date,
    Datetime,
    Expr,
    Float64,
    Int64,
    List,
    Object,
    Series,
    Struct,
    Utf8,
    all_horizontal,
    col,
    concat,
    lit,
    struct,
    when,
)
from polars._typing import (
    IntoExpr,
    IntoExprColumn,
    JoinStrategy,
    JoinValidation,
    PolarsDataType,
    SchemaDict,
    TimeUnit,
)
from polars.datatypes import DataType
from polars.exceptions import (
    ColumnNotFoundError,
    OutOfBoundsError,
    PolarsInefficientMapWarning,
)
from polars.testing import assert_frame_equal
from typing_extensions import override

from utilities.dataclasses import _YieldFieldsInstance, yield_fields
from utilities.errors import ImpossibleCaseError
from utilities.functions import (
    is_dataclass_class,
    is_dataclass_instance,
    is_iterable_of,
    make_isinstance,
)
from utilities.iterables import (
    CheckIterablesEqualError,
    CheckMappingsEqualError,
    CheckSubSetError,
    CheckSuperMappingError,
    CheckSuperSetError,
    OneEmptyError,
    OneNonUniqueError,
    always_iterable,
    check_iterables_equal,
    check_mappings_equal,
    check_subset,
    check_supermapping,
    check_superset,
    is_iterable_not_str,
    one,
)
from utilities.math import (
    CheckIntegerError,
    _EWMParameters,
    check_integer,
    ewm_parameters,
)
from utilities.reprlib import get_repr
from utilities.sentinel import Sentinel
from utilities.types import Dataclass, MaybeIterable, StrMapping, ZoneInfoLike
from utilities.typing import (
    get_args,
    get_type_hints,
    is_frozenset_type,
    is_list_type,
    is_literal_type,
    is_optional_type,
    is_set_type,
)
from utilities.warnings import suppress_warnings
from utilities.zoneinfo import UTC, ensure_time_zone, get_time_zone_name

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Iterator, Sequence
    from collections.abc import Set as AbstractSet


_T = TypeVar("_T")
_TDataclass = TypeVar("_TDataclass", bound=Dataclass)
DatetimeHongKong = Datetime(time_zone="Asia/Hong_Kong")
DatetimeTokyo = Datetime(time_zone="Asia/Tokyo")
DatetimeUSCentral = Datetime(time_zone="US/Central")
DatetimeUSEastern = Datetime(time_zone="US/Eastern")
DatetimeUTC = Datetime(time_zone="UTC")
ExprLike: TypeAlias = Expr | str


##


def append_dataclass(df: DataFrame, obj: Dataclass, /) -> DataFrame:
    """Append a dataclass object to a DataFrame."""
    non_null_fields = {k: v for k, v in asdict(obj).items() if v is not None}
    try:
        check_subset(non_null_fields, df.columns)
    except CheckSubSetError as error:
        raise AppendDataClassError(
            left=error.left, right=error.right, extra=error.extra
        ) from None
    row_cols = set(df.columns) & set(non_null_fields)
    row = dataclass_to_dataframe(obj).select(*row_cols)
    return concat([df, row], how="diagonal")


@dataclass(kw_only=True, slots=True)
class AppendDataClassError(Exception, Generic[_T]):
    left: AbstractSet[_T]
    right: AbstractSet[_T]
    extra: AbstractSet[_T]

    @override
    def __str__(self) -> str:
        return f"Dataclass fields {get_repr(self.left)} must be a subset of DataFrame columns {get_repr(self.right)}; dataclass had extra items {get_repr(self.extra)}"


##


def are_frames_equal(
    left: DataFrame,
    right: DataFrame,
    /,
    *,
    check_row_order: bool = True,
    check_column_order: bool = True,
    check_dtypes: bool = True,
    check_exact: bool = False,
    rtol: float = 1e-5,
    atol: float = 1e-8,
    categorical_as_str: bool = False,
) -> bool:
    """Check if two DataFrames are equal."""
    try:
        assert_frame_equal(
            left,
            right,
            check_row_order=check_row_order,
            check_column_order=check_column_order,
            check_dtypes=check_dtypes,
            check_exact=check_exact,
            rtol=rtol,
            atol=atol,
            categorical_as_str=categorical_as_str,
        )
    except AssertionError:
        return False
    return True


##


@overload
def ceil_datetime(column: ExprLike, every: ExprLike, /) -> Expr: ...
@overload
def ceil_datetime(column: Series, every: ExprLike, /) -> Series: ...
def ceil_datetime(column: IntoExprColumn, every: ExprLike, /) -> Expr | Series:
    """Compute the `ceil` of a datetime column."""
    column = ensure_expr_or_series(column)
    rounded = column.dt.round(every)
    ceil = (
        when(column <= rounded)
        .then(rounded)
        .otherwise(column.dt.offset_by(every).dt.round(every))
    )
    if isinstance(column, Expr):
        return ceil
    return DataFrame().with_columns(ceil.alias(column.name))[column.name]


##


def check_polars_dataframe(
    df: DataFrame,
    /,
    *,
    columns: Iterable[str] | None = None,
    dtypes: Iterable[PolarsDataType] | None = None,
    height: int | tuple[int, float] | None = None,
    min_height: int | None = None,
    max_height: int | None = None,
    predicates: Mapping[str, Callable[[Any], bool]] | None = None,
    schema_list: SchemaDict | None = None,
    schema_set: SchemaDict | None = None,
    schema_subset: SchemaDict | None = None,
    shape: tuple[int, int] | None = None,
    sorted: MaybeIterable[IntoExpr] | None = None,  # noqa: A002
    unique: MaybeIterable[IntoExpr] | None = None,
    width: int | None = None,
) -> None:
    """Check the properties of a DataFrame."""
    _check_polars_dataframe_height(
        df, equal_or_approx=height, min=min_height, max=max_height
    )
    if columns is not None:
        _check_polars_dataframe_columns(df, columns)
    if dtypes is not None:
        _check_polars_dataframe_dtypes(df, dtypes)
    if predicates is not None:
        _check_polars_dataframe_predicates(df, predicates)
    if schema_list is not None:
        _check_polars_dataframe_schema_list(df, schema_list)
    if schema_set is not None:
        _check_polars_dataframe_schema_set(df, schema_set)
    if schema_subset is not None:
        _check_polars_dataframe_schema_subset(df, schema_subset)
    if shape is not None:
        _check_polars_dataframe_shape(df, shape)
    if sorted is not None:
        _check_polars_dataframe_sorted(df, sorted)
    if unique is not None:
        _check_polars_dataframe_unique(df, unique)
    if width is not None:
        _check_polars_dataframe_width(df, width)


@dataclass(kw_only=True, slots=True)
class CheckPolarsDataFrameError(Exception):
    df: DataFrame


def _check_polars_dataframe_columns(df: DataFrame, columns: Iterable[str], /) -> None:
    columns = list(columns)
    try:
        check_iterables_equal(df.columns, columns)
    except CheckIterablesEqualError as error:
        raise _CheckPolarsDataFrameColumnsError(df=df, columns=columns) from error


@dataclass(kw_only=True, slots=True)
class _CheckPolarsDataFrameColumnsError(CheckPolarsDataFrameError):
    columns: Sequence[str]

    @override
    def __str__(self) -> str:
        return f"DataFrame must have columns {get_repr(self.columns)}; got {get_repr(self.df.columns)}:\n\n{self.df}"


def _check_polars_dataframe_dtypes(
    df: DataFrame, dtypes: Iterable[PolarsDataType], /
) -> None:
    try:
        check_iterables_equal(df.dtypes, dtypes)
    except CheckIterablesEqualError as error:
        raise _CheckPolarsDataFrameDTypesError(df=df, dtypes=dtypes) from error


@dataclass(kw_only=True, slots=True)
class _CheckPolarsDataFrameDTypesError(CheckPolarsDataFrameError):
    dtypes: Iterable[PolarsDataType]

    @override
    def __str__(self) -> str:
        return f"DataFrame must have dtypes {get_repr(self.dtypes)}; got {get_repr(self.df.dtypes)}:\n\n{self.df}"


def _check_polars_dataframe_height(
    df: DataFrame,
    /,
    *,
    equal_or_approx: int | tuple[int, float] | None = None,
    min: int | None = None,  # noqa: A002
    max: int | None = None,  # noqa: A002
) -> None:
    try:
        check_integer(df.height, equal_or_approx=equal_or_approx, min=min, max=max)
    except CheckIntegerError as error:
        raise _CheckPolarsDataFrameHeightError(df=df) from error


@dataclass(kw_only=True, slots=True)
class _CheckPolarsDataFrameHeightError(CheckPolarsDataFrameError):
    @override
    def __str__(self) -> str:
        return f"DataFrame must satisfy the height requirements; got {self.df.height}:\n\n{self.df}"


def _check_polars_dataframe_predicates(
    df: DataFrame, predicates: Mapping[str, Callable[[Any], bool]], /
) -> None:
    missing: set[str] = set()
    failed: set[str] = set()
    for column, predicate in predicates.items():
        try:
            sr = df[column]
        except ColumnNotFoundError:
            missing.add(column)
        else:
            if not sr.map_elements(predicate, return_dtype=Boolean).all():
                failed.add(column)
    if (len(missing) >= 1) or (len(failed)) >= 1:
        raise _CheckPolarsDataFramePredicatesError(
            df=df, predicates=predicates, missing=missing, failed=failed
        )


@dataclass(kw_only=True, slots=True)
class _CheckPolarsDataFramePredicatesError(CheckPolarsDataFrameError):
    predicates: Mapping[str, Callable[[Any], bool]]
    missing: AbstractSet[str]
    failed: AbstractSet[str]

    @override
    def __str__(self) -> str:
        parts = list(self._yield_parts())
        match parts:
            case (desc,):
                pass
            case first, second:
                desc = f"{first} and {second}"
            case _:  # pragma: no cover
                raise ImpossibleCaseError(case=[f"{parts=}"])
        return f"DataFrame must satisfy the predicates; {desc}:\n\n{self.df}"

    def _yield_parts(self) -> Iterator[str]:
        if len(self.missing) >= 1:
            yield f"missing columns were {get_repr(self.missing)}"
        if len(self.failed) >= 1:
            yield f"failed predicates were {get_repr(self.failed)}"


def _check_polars_dataframe_schema_list(df: DataFrame, schema: SchemaDict, /) -> None:
    try:
        _check_polars_dataframe_schema_set(df, schema)
    except _CheckPolarsDataFrameSchemaSetError as error:
        raise _CheckPolarsDataFrameSchemaListError(df=df, schema=schema) from error
    try:
        _check_polars_dataframe_columns(df, schema)
    except _CheckPolarsDataFrameColumnsError as error:
        raise _CheckPolarsDataFrameSchemaListError(df=df, schema=schema) from error


@dataclass(kw_only=True, slots=True)
class _CheckPolarsDataFrameSchemaListError(CheckPolarsDataFrameError):
    schema: SchemaDict

    @override
    def __str__(self) -> str:
        return f"DataFrame must have schema {get_repr(self.schema)} (ordered); got {get_repr(self.df.schema)}:\n\n{self.df}"


def _check_polars_dataframe_schema_set(df: DataFrame, schema: SchemaDict, /) -> None:
    try:
        check_mappings_equal(df.schema, schema)
    except CheckMappingsEqualError as error:
        raise _CheckPolarsDataFrameSchemaSetError(df=df, schema=schema) from error


@dataclass(kw_only=True, slots=True)
class _CheckPolarsDataFrameSchemaSetError(CheckPolarsDataFrameError):
    schema: SchemaDict

    @override
    def __str__(self) -> str:
        return f"DataFrame must have schema {get_repr(self.schema)} (unordered); got {get_repr(self.df.schema)}:\n\n{self.df}"


def _check_polars_dataframe_schema_subset(df: DataFrame, schema: SchemaDict, /) -> None:
    try:
        check_supermapping(df.schema, schema)
    except CheckSuperMappingError as error:
        raise _CheckPolarsDataFrameSchemaSubsetError(df=df, schema=schema) from error


@dataclass(kw_only=True, slots=True)
class _CheckPolarsDataFrameSchemaSubsetError(CheckPolarsDataFrameError):
    schema: SchemaDict

    @override
    def __str__(self) -> str:
        return f"DataFrame schema must include {get_repr(self.schema)} (unordered); got {get_repr(self.df.schema)}:\n\n{self.df}"


def _check_polars_dataframe_shape(df: DataFrame, shape: tuple[int, int], /) -> None:
    if df.shape != shape:
        raise _CheckPolarsDataFrameShapeError(df=df, shape=shape) from None


@dataclass(kw_only=True, slots=True)
class _CheckPolarsDataFrameShapeError(CheckPolarsDataFrameError):
    shape: tuple[int, int]

    @override
    def __str__(self) -> str:
        return (
            f"DataFrame must have shape {self.shape}; got {self.df.shape}:\n\n{self.df}"
        )


def _check_polars_dataframe_sorted(
    df: DataFrame, by: MaybeIterable[IntoExpr], /
) -> None:
    by_use = cast(
        IntoExpr | list[IntoExpr], list(by) if is_iterable_not_str(by) else by
    )
    df_sorted = df.sort(by_use)
    try:
        assert_frame_equal(df, df_sorted)
    except AssertionError as error:
        raise _CheckPolarsDataFrameSortedError(df=df, by=by_use) from error


@dataclass(kw_only=True, slots=True)
class _CheckPolarsDataFrameSortedError(CheckPolarsDataFrameError):
    by: IntoExpr | list[IntoExpr]

    @override
    def __str__(self) -> str:
        return f"DataFrame must be sorted on {get_repr(self.by)}:\n\n{self.df}"


def _check_polars_dataframe_unique(
    df: DataFrame, by: MaybeIterable[IntoExpr], /
) -> None:
    by_use = cast(
        IntoExpr | list[IntoExpr], list(by) if is_iterable_not_str(by) else by
    )
    if df.select(by_use).is_duplicated().any():
        raise _CheckPolarsDataFrameUniqueError(df=df, by=by_use)


@dataclass(kw_only=True, slots=True)
class _CheckPolarsDataFrameUniqueError(CheckPolarsDataFrameError):
    by: IntoExpr | list[IntoExpr]

    @override
    def __str__(self) -> str:
        return f"DataFrame must be unique on {get_repr(self.by)}:\n\n{self.df}"


def _check_polars_dataframe_width(df: DataFrame, width: int, /) -> None:
    if df.width != width:
        raise _CheckPolarsDataFrameWidthError(df=df, width=width)


@dataclass(kw_only=True, slots=True)
class _CheckPolarsDataFrameWidthError(CheckPolarsDataFrameError):
    width: int

    @override
    def __str__(self) -> str:
        return (
            f"DataFrame must have width {self.width}; got {self.df.width}:\n\n{self.df}"
        )


##


def collect_series(expr: Expr, /) -> Series:
    """Collect a column expression into a Series."""
    data = DataFrame().with_columns(expr)
    return data[one(data.columns)]


##


def columns_to_dict(df: DataFrame, key: str, value: str, /) -> dict[Any, Any]:
    """Map a pair of columns into a dictionary. Must be unique on `key`."""
    col_key = df[key]
    if col_key.is_duplicated().any():
        raise ColumnsToDictError(df=df, key=key)
    col_value = df[value]
    return dict(zip(col_key, col_value, strict=True))


@dataclass(kw_only=True, slots=True)
class ColumnsToDictError(Exception):
    df: DataFrame
    key: str

    @override
    def __str__(self) -> str:
        return f"DataFrame must be unique on {self.key!r}:\n\n{self.df}"


##


@overload
def convert_time_zone(obj: Series, /, *, time_zone: ZoneInfoLike = ...) -> Series: ...
@overload
def convert_time_zone(
    obj: DataFrame, /, *, time_zone: ZoneInfoLike = ...
) -> DataFrame: ...
def convert_time_zone(
    obj: Series | DataFrame, /, *, time_zone: ZoneInfoLike = UTC
) -> Series | DataFrame:
    """Convert the time zone(s) of a Series or Dataframe."""
    return map_over_columns(partial(_convert_time_zone_one, time_zone=time_zone), obj)


def _convert_time_zone_one(sr: Series, /, *, time_zone: ZoneInfoLike = UTC) -> Series:
    if isinstance(sr.dtype, Datetime):
        return sr.dt.convert_time_zone(get_time_zone_name(time_zone))
    return sr


##


def dataclass_to_dataframe(
    objs: MaybeIterable[Dataclass],
    /,
    *,
    globalns: StrMapping | None = None,
    localns: StrMapping | None = None,
) -> DataFrame:
    """Convert a dataclass/es into a DataFrame."""
    objs = list(always_iterable(objs))
    try:
        _ = one(set(map(type, objs)))
    except OneEmptyError:
        raise _DataClassToDataFrameEmptyError from None
    except OneNonUniqueError as error:
        raise _DataClassToDataFrameNonUniqueError(
            objs=objs, first=error.first, second=error.second
        ) from None
    data = list(map(asdict, objs))
    first, *_ = objs
    schema = dataclass_to_schema(first, globalns=globalns, localns=localns)
    df = DataFrame(data, schema=schema, orient="row")
    return map_over_columns(_dataclass_to_dataframe_uuid, df)


def _dataclass_to_dataframe_uuid(series: Series, /) -> Series:
    if series.dtype == Object:
        is_path = series.map_elements(make_isinstance(Path), return_dtype=Boolean).all()
        is_uuid = series.map_elements(make_isinstance(UUID), return_dtype=Boolean).all()
        if is_path or is_uuid:
            with suppress_warnings(category=PolarsInefficientMapWarning):
                return series.map_elements(str, return_dtype=Utf8)
        else:  # pragma: no cover
            msg = f"{is_path=}, f{is_uuid=}"
            raise NotImplementedError(msg)
    return series


@dataclass(kw_only=True, slots=True)
class DataClassToDataFrameError(Exception): ...


@dataclass(kw_only=True, slots=True)
class _DataClassToDataFrameEmptyError(DataClassToDataFrameError):
    @override
    def __str__(self) -> str:
        return "At least 1 dataclass must be given; got 0"


@dataclass(kw_only=True, slots=True)
class _DataClassToDataFrameNonUniqueError(DataClassToDataFrameError):
    objs: list[Dataclass]
    first: Any
    second: Any

    @override
    def __str__(self) -> str:
        return f"Iterable {get_repr(self.objs)} must contain exactly one class; got {self.first}, {self.second} and perhaps more"


##


def dataclass_to_schema(
    obj: Dataclass,
    /,
    *,
    globalns: StrMapping | None = None,
    localns: StrMapping | None = None,
) -> SchemaDict:
    """Cast a dataclass as a schema dict."""
    out: dict[str, Any] = {}
    for field in yield_fields(obj, globalns=globalns, localns=localns):
        if is_dataclass_instance(field.value):
            dtypes = dataclass_to_schema(
                field.value, globalns=globalns, localns=localns
            )
            dtype = struct_dtype(**dtypes)
        elif field.type_ is dt.datetime:
            field_use = cast(_YieldFieldsInstance[dt.datetime], field)
            if field_use.value.tzinfo is None:
                dtype = Datetime
            else:
                dtype = zoned_datetime(
                    time_zone=ensure_time_zone(field_use.value.tzinfo)
                )
        else:
            dtype = _dataclass_to_schema_one(
                field.type_, globalns=globalns, localns=localns
            )
        out[field.name] = dtype
    return out


def _dataclass_to_schema_one(
    obj: Any,
    /,
    *,
    globalns: StrMapping | None = None,
    localns: StrMapping | None = None,
) -> PolarsDataType:
    if obj is bool:
        return Boolean
    if obj is int:
        return Int64
    if obj is float:
        return Float64
    if obj is str:
        return Utf8
    if obj is dt.date:
        return Date
    if obj in {Path, UUID}:
        return Object
    if isinstance(obj, type) and issubclass(obj, enum.Enum):
        return pl.Enum([e.name for e in obj])
    if is_dataclass_class(obj):
        out: dict[str, Any] = {}
        for field in yield_fields(obj, globalns=globalns, localns=localns):
            out[field.name] = _dataclass_to_schema_one(
                field.type_, globalns=globalns, localns=localns
            )
        return struct_dtype(**out)
    if is_frozenset_type(obj) or is_list_type(obj) or is_set_type(obj):
        inner_type = one(get_args(obj))
        inner_dtype = _dataclass_to_schema_one(
            inner_type, globalns=globalns, localns=localns
        )
        return List(inner_dtype)
    if is_literal_type(obj):
        return pl.Enum(get_args(obj))
    if is_optional_type(obj):
        inner_type = one(get_args(obj))
        return _dataclass_to_schema_one(inner_type, globalns=globalns, localns=localns)
    msg = f"{obj=}"
    raise NotImplementedError(msg)


##


def drop_null_struct_series(series: Series, /) -> Series:
    """Drop nulls in a struct-dtype Series as per the <= 1.1 definition."""
    try:
        is_not_null = is_not_null_struct_series(series)
    except IsNotNullStructSeriesError as error:
        raise DropNullStructSeriesError(series=error.series) from None
    return series.filter(is_not_null)


@dataclass(kw_only=True, slots=True)
class DropNullStructSeriesError(Exception):
    series: Series

    @override
    def __str__(self) -> str:
        return f"Series must have Struct-dtype; got {self.series.dtype}"


##


@overload
def ensure_expr_or_series(column: ExprLike, /) -> Expr: ...
@overload
def ensure_expr_or_series(column: Series, /) -> Series: ...
def ensure_expr_or_series(column: IntoExprColumn, /) -> Expr | Series:
    """Ensure a column expression or Series is returned."""
    return col(column) if isinstance(column, str) else column


##


@overload
def floor_datetime(column: ExprLike, every: ExprLike, /) -> Expr: ...
@overload
def floor_datetime(column: Series, every: ExprLike, /) -> Series: ...
def floor_datetime(column: IntoExprColumn, every: ExprLike, /) -> Expr | Series:
    """Compute the `floor` of a datetime column."""
    column = ensure_expr_or_series(column)
    rounded = column.dt.round(every)
    floor = (
        when(column >= rounded)
        .then(rounded)
        .otherwise(column.dt.offset_by("-" + every).dt.round(every))
    )
    if isinstance(column, Expr):
        return floor
    return DataFrame().with_columns(floor.alias(column.name))[column.name]


##


def get_data_type_or_series_time_zone(
    dtype_or_series: DataType | Series, /
) -> ZoneInfo:
    """Get the time zone of a dtype/series."""
    if isinstance(dtype_or_series, DataType):
        dtype = dtype_or_series
    else:
        dtype = dtype_or_series.dtype
    if not isinstance(dtype, Datetime):
        raise _GetDataTypeOrSeriesTimeZoneNotDatetimeError(dtype=dtype)
    if dtype.time_zone is None:
        raise _GetDataTypeOrSeriesTimeZoneNotZonedError(dtype=dtype)
    return ZoneInfo(dtype.time_zone)


@dataclass(kw_only=True, slots=True)
class GetDataTypeOrSeriesTimeZoneError(Exception):
    dtype: DataType


@dataclass(kw_only=True, slots=True)
class _GetDataTypeOrSeriesTimeZoneNotDatetimeError(GetDataTypeOrSeriesTimeZoneError):
    @override
    def __str__(self) -> str:
        return f"Data type must be Datetime; got {self.dtype}"


@dataclass(kw_only=True, slots=True)
class _GetDataTypeOrSeriesTimeZoneNotZonedError(GetDataTypeOrSeriesTimeZoneError):
    @override
    def __str__(self) -> str:
        return f"Data type must be zoned; got {self.dtype}"


##


def is_not_null_struct_series(series: Series, /) -> Series:
    """Check if a struct-dtype Series is not null as per the <= 1.1 definition."""
    try:
        return ~is_null_struct_series(series)
    except IsNullStructSeriesError as error:
        raise IsNotNullStructSeriesError(series=error.series) from None


@dataclass(kw_only=True, slots=True)
class IsNotNullStructSeriesError(Exception):
    series: Series

    @override
    def __str__(self) -> str:
        return f"Series must have Struct-dtype; got {self.series.dtype}"


##


def is_null_struct_series(series: Series, /) -> Series:
    """Check if a struct-dtype Series is null as per the <= 1.1 definition."""
    if not isinstance(series.dtype, Struct):
        raise IsNullStructSeriesError(series=series)
    paths = _is_null_struct_series_one(series.dtype)
    paths = list(paths)
    exprs = map(_is_null_struct_to_expr, paths)
    expr = all_horizontal(*exprs)
    return (
        series.struct.unnest().with_columns(_result=expr)["_result"].rename(series.name)
    )


def _is_null_struct_series_one(
    dtype: Struct, /, *, root: Iterable[str] = ()
) -> Iterator[Sequence[str]]:
    for field in dtype.fields:
        name = field.name
        inner = field.dtype
        path = list(chain(root, [name]))
        if isinstance(inner, Struct):
            yield from _is_null_struct_series_one(inner, root=path)
        else:
            yield path


def _is_null_struct_to_expr(path: Iterable[str], /) -> Expr:
    head, *tail = path
    return reduce(_is_null_struct_to_expr_reducer, tail, col(head)).is_null()


def _is_null_struct_to_expr_reducer(expr: Expr, path: str, /) -> Expr:
    return expr.struct[path]


@dataclass(kw_only=True, slots=True)
class IsNullStructSeriesError(Exception):
    series: Series

    @override
    def __str__(self) -> str:
        return f"Series must have Struct-dtype; got {self.series.dtype}"


##


def join(
    df: DataFrame,
    *dfs: DataFrame,
    on: MaybeIterable[str | Expr],
    how: JoinStrategy = "inner",
    validate: JoinValidation = "m:m",
) -> DataFrame:
    """Join a set of DataFrames."""
    on_use = on if isinstance(on, str | Expr) else list(on)

    def inner(left: DataFrame, right: DataFrame, /) -> DataFrame:
        return left.join(right, on=on_use, how=how, validate=validate)

    return reduce(inner, chain([df], dfs))


##


@overload
def map_over_columns(func: Callable[[Series], Series], obj: Series, /) -> Series: ...
@overload
def map_over_columns(
    func: Callable[[Series], Series], obj: DataFrame, /
) -> DataFrame: ...
def map_over_columns(
    func: Callable[[Series], Series], obj: Series | DataFrame, /
) -> Series | DataFrame:
    """Map a function over the columns of a Struct-Series/DataFrame."""
    match obj:
        case Series() as series:
            return _map_over_series_one(func, series)
        case DataFrame() as df:
            return df.select(*(_map_over_series_one(func, df[c]) for c in df.columns))
        case _ as never:  # pyright: ignore[reportUnnecessaryComparison]
            assert_never(never)


def _map_over_series_one(func: Callable[[Series], Series], series: Series, /) -> Series:
    if isinstance(series.dtype, Struct):
        unnested = series.struct.unnest()
        name = series.name
        return map_over_columns(func, unnested).select(struct("*").alias(name))[name]
    return func(series)


##


def nan_sum_agg(column: str | Expr, /, *, dtype: PolarsDataType | None = None) -> Expr:
    """Nan sum aggregation."""
    col_use = col(column) if isinstance(column, str) else column
    return (
        when(col_use.is_not_null().any())
        .then(col_use.sum())
        .otherwise(lit(None, dtype=dtype))
    )


##


def nan_sum_cols(
    column: str | Expr, *columns: str | Expr, dtype: PolarsDataType | None = None
) -> Expr:
    """Nan sum across columns."""
    all_columns = chain([column], columns)
    all_exprs = (
        col(column) if isinstance(column, str) else column for column in all_columns
    )

    def func(x: Expr, y: Expr, /) -> Expr:
        return (
            when(x.is_not_null() & y.is_not_null())
            .then(x + y)
            .when(x.is_not_null() & y.is_null())
            .then(x)
            .when(x.is_null() & y.is_not_null())
            .then(y)
            .otherwise(lit(None, dtype=dtype))
        )

    return reduce(func, all_exprs)


##


@overload
def replace_time_zone(
    obj: Series, /, *, time_zone: ZoneInfoLike | None = ...
) -> Series: ...
@overload
def replace_time_zone(
    obj: DataFrame, /, *, time_zone: ZoneInfoLike | None = ...
) -> DataFrame: ...
def replace_time_zone(
    obj: Series | DataFrame, /, *, time_zone: ZoneInfoLike | None = UTC
) -> Series | DataFrame:
    """Replace the time zone(s) of a Series or Dataframe."""
    return map_over_columns(partial(_replace_time_zone_one, time_zone=time_zone), obj)


def _replace_time_zone_one(
    sr: Series, /, *, time_zone: ZoneInfoLike | None = UTC
) -> Series:
    if isinstance(sr.dtype, Datetime):
        time_zone_use = None if time_zone is None else get_time_zone_name(time_zone)
        return sr.dt.replace_time_zone(time_zone_use)
    return sr


##


@overload
def rolling_parameters(
    *,
    s_window: int,
    e_com: None = None,
    e_span: None = None,
    e_half_life: None = None,
    e_alpha: None = None,
    min_periods: int | None = None,
) -> RollingParametersSimple: ...
@overload
def rolling_parameters(
    *,
    s_window: None = None,
    e_com: float | None = None,
    e_span: float | None = None,
    e_half_life: float | None = None,
    e_alpha: float | None = None,
    min_periods: int,
) -> RollingParametersExponential: ...
@overload
def rolling_parameters(
    *,
    s_window: int | None = None,
    e_com: float | None = None,
    e_span: float | None = None,
    e_half_life: float | None = None,
    e_alpha: float | None = None,
    min_periods: int | None = None,
) -> RollingParametersSimple | RollingParametersExponential: ...
def rolling_parameters(
    *,
    s_window: int | None = None,
    e_com: float | None = None,
    e_span: float | None = None,
    e_half_life: float | None = None,
    e_alpha: float | None = None,
    min_periods: int | None = None,
) -> RollingParametersSimple | RollingParametersExponential:
    """Resolve a set of rolling parameters."""
    if (
        (s_window is not None)
        and (e_com is None)
        and (e_span is None)
        and (e_half_life is None)
        and (e_alpha is None)
    ):
        return RollingParametersSimple(window=s_window, min_periods=min_periods)
    if (s_window is None) and (
        (e_com is not None)
        or (e_span is not None)
        or (e_half_life is not None)
        or (e_alpha is not None)
    ):
        if min_periods is None:
            raise _RollingParametersMinPeriodsError(
                e_com=e_com,
                e_span=e_span,
                e_half_life=e_half_life,
                e_alpha=e_alpha,
                min_periods=min_periods,
            )
        params = ewm_parameters(
            com=e_com, span=e_span, half_life=e_half_life, alpha=e_alpha
        )
        return RollingParametersExponential(
            com=params.com,
            span=params.span,
            half_life=params.half_life,
            alpha=params.alpha,
            min_periods=min_periods,
        )
    raise _RollingParametersArgumentsError(
        s_window=s_window,
        e_com=e_com,
        e_span=e_span,
        e_half_life=e_half_life,
        e_alpha=e_alpha,
    )


@dataclass(kw_only=True, slots=True)
class RollingParametersSimple:
    window: int
    min_periods: int | None = None


@dataclass(kw_only=True, slots=True)
class RollingParametersExponential(_EWMParameters):
    min_periods: int


@dataclass(kw_only=True, slots=True)
class RollingParametersError(Exception):
    s_window: int | None = None
    e_com: float | None = None
    e_span: float | None = None
    e_half_life: float | None = None
    e_alpha: float | None = None


@dataclass(kw_only=True, slots=True)
class _RollingParametersArgumentsError(RollingParametersError):
    @override
    def __str__(self) -> str:
        return f"Exactly one of simple window, exponential center of mass (γ), exponential span (θ), exponential half-life (λ) or exponential smoothing factor (α) must be given; got s_window={self.s_window}, γ={self.e_com}, θ={self.e_span}, λ={self.e_half_life} and α={self.e_alpha}"  # noqa: RUF001


@dataclass(kw_only=True, slots=True)
class _RollingParametersMinPeriodsError(RollingParametersError):
    min_periods: int | None = None

    @override
    def __str__(self) -> str:
        return f"Exponential rolling requires 'min_periods' to be set; got {self.min_periods}"


##


def set_first_row_as_columns(df: DataFrame, /) -> DataFrame:
    """Set the first row of a DataFrame as its columns."""
    try:
        row = df.row(0)
    except OutOfBoundsError:
        raise SetFirstRowAsColumnsError(df=df) from None
    mapping = dict(zip(df.columns, row, strict=True))
    return df[1:].rename(mapping)


@dataclass(kw_only=True, slots=True)
class SetFirstRowAsColumnsError(Exception):
    df: DataFrame

    @override
    def __str__(self) -> str:
        return f"DataFrame must have at least 1 row; got {self.df}"


##


def struct_dtype(**kwargs: PolarsDataType) -> Struct:
    """Construct a Struct data type from a set of keyword arguments."""
    return Struct(kwargs)


##


def struct_from_dataclass(
    cls: type[Dataclass],
    /,
    *,
    globalns: StrMapping | None = None,
    localns: StrMapping | None = None,
    time_zone: ZoneInfoLike | None = None,
) -> Struct:
    """Construct the Struct data type for a dataclass."""
    if not is_dataclass_class(cls):
        raise _StructFromDataClassNotADataclassError(cls=cls)
    anns = get_type_hints(cls, globalns=globalns, localns=localns)
    data_types = {
        k: _struct_from_dataclass_one(v, time_zone=time_zone) for k, v in anns.items()
    }
    return Struct(data_types)


def _struct_from_dataclass_one(
    ann: Any, /, *, time_zone: ZoneInfoLike | None = None
) -> PolarsDataType:
    mapping = {bool: Boolean, dt.date: Date, float: Float64, int: Int64, str: Utf8}
    with suppress(KeyError):
        return mapping[ann]
    if ann is dt.datetime:
        if time_zone is None:
            raise _StructFromDataClassTimeZoneMissingError
        return zoned_datetime(time_zone=time_zone)
    if is_dataclass_class(ann):
        return struct_from_dataclass(ann, time_zone=time_zone)
    if (isinstance(ann, type) and issubclass(ann, enum.Enum)) or (
        is_literal_type(ann) and is_iterable_of(get_args(ann), str)
    ):
        return Utf8
    if is_optional_type(ann):
        return _struct_from_dataclass_one(one(get_args(ann)), time_zone=time_zone)
    if is_frozenset_type(ann) or is_list_type(ann) or is_set_type(ann):
        return List(_struct_from_dataclass_one(one(get_args(ann)), time_zone=time_zone))
    raise _StructFromDataClassTypeError(ann=ann)


@dataclass(kw_only=True, slots=True)
class StructFromDataClassError(Exception): ...


@dataclass(kw_only=True, slots=True)
class _StructFromDataClassNotADataclassError(StructFromDataClassError):
    cls: type[Dataclass]

    @override
    def __str__(self) -> str:
        return f"Object must be a dataclass; got {self.cls}"


@dataclass(kw_only=True, slots=True)
class _StructFromDataClassTimeZoneMissingError(StructFromDataClassError):
    @override
    def __str__(self) -> str:
        return "Time-zone must be given"


@dataclass(kw_only=True, slots=True)
class _StructFromDataClassTypeError(StructFromDataClassError):
    ann: Any

    @override
    def __str__(self) -> str:
        return f"Unsupported type: {self.ann}"


##


def unique_element(column: ExprLike, /) -> Expr:
    """Get the unique element in a list."""
    column = ensure_expr_or_series(column)
    return when(column.list.len() == 1).then(column.list.first())


##


def yield_rows_as_dataclasses(
    df: DataFrame,
    cls: type[_TDataclass],
    /,
    *,
    globalns: StrMapping | None = None,
    localns: StrMapping | None = None,
    check_types: Literal["none", "first", "all"] = "first",
) -> Iterator[_TDataclass]:
    """Yield the rows of a DataFrame as dataclasses."""
    from dacite import from_dict
    from dacite.exceptions import WrongTypeError

    columns = df.columns
    required: set[str] = set()
    for field in yield_fields(cls, globalns=globalns, localns=localns):
        if isinstance(field.default, Sentinel) and isinstance(
            field.default_factory, Sentinel
        ):
            required.add(field.name)
    try:
        check_superset(columns, required)
    except CheckSuperSetError as error:
        raise _YieldRowsAsDataClassesColumnsSuperSetError(
            df=df, cls=cls, left=error.left, right=error.right, extra=error.extra
        ) from None
    rows = df.iter_rows(named=True)
    match check_types:
        case "none":
            yield from _yield_rows_as_dataclasses_no_check_types(rows, cls)
        case "first":
            try:
                first = next(rows)
            except StopIteration:
                return
            try:
                yield from_dict(cls, first)
            except WrongTypeError as error:
                raise _YieldRowsAsDataClassesWrongTypeError(
                    df=df, cls=cls, msg=str(error)
                ) from None
            yield from _yield_rows_as_dataclasses_no_check_types(rows, cls)
        case "all":
            try:
                for row in rows:
                    yield from_dict(cls, row)
            except WrongTypeError as error:
                raise _YieldRowsAsDataClassesWrongTypeError(
                    df=df, cls=cls, msg=str(error)
                ) from None
        case _ as never:  # pyright: ignore[reportUnnecessaryComparison]
            assert_never(never)


def _yield_rows_as_dataclasses_no_check_types(
    rows: Iterator[dict[str, Any]], cls: type[_TDataclass], /
) -> Iterator[_TDataclass]:
    """Yield the rows of a DataFrame as dataclasses without type checking."""
    from dacite import Config, from_dict

    config = Config(check_types=False)
    for row in rows:
        yield from_dict(cls, row, config=config)


@dataclass(kw_only=True, slots=True)
class YieldRowsAsDataClassesError(Exception):
    df: DataFrame
    cls: type[Dataclass]


@dataclass(kw_only=True, slots=True)
class _YieldRowsAsDataClassesColumnsSuperSetError(YieldRowsAsDataClassesError):
    left: AbstractSet[str]
    right: AbstractSet[str]
    extra: AbstractSet[str]

    @override
    def __str__(self) -> str:
        return f"DataFrame columns {get_repr(self.left)} must be a superset of dataclass fields {get_repr(self.right)}; dataclass had extra fields {get_repr(self.extra)}."


@dataclass(kw_only=True, slots=True)
class _YieldRowsAsDataClassesWrongTypeError(YieldRowsAsDataClassesError):
    msg: str

    @override
    def __str__(self) -> str:
        return self.msg


##


@overload
def yield_struct_series_elements(
    series: Series, /, *, strict: Literal[True]
) -> Iterator[Mapping[str, Any]]: ...
@overload
def yield_struct_series_elements(
    series: Series, /, *, strict: bool = False
) -> Iterator[Mapping[str, Any] | None]: ...
def yield_struct_series_elements(
    series: Series, /, *, strict: bool = False
) -> Iterator[Mapping[str, Any] | None]:
    """Yield the elements of a struct-dtype Series as optional mappings."""
    if not isinstance(series.dtype, Struct):
        raise _YieldStructSeriesElementsDTypeError(series=series)
    if strict and series.is_null().any():
        raise _YieldStructSeriesElementsNullElementsError(series=series)
    for value in series:
        yield _yield_struct_series_element_remove_nulls(value)


def _yield_struct_series_element_remove_nulls(obj: Any, /) -> Any:
    if not _yield_struct_series_element_is_mapping_of_str(obj):
        return obj
    if any(_yield_struct_series_element_is_mapping_of_str(v) for v in obj.values()):
        result = {
            k: _yield_struct_series_element_remove_nulls(v) for k, v in obj.items()
        }
        if result == obj:
            return result
        return _yield_struct_series_element_remove_nulls(result)
    return None if all(v is None for v in obj.values()) else obj


def _yield_struct_series_element_is_mapping_of_str(
    obj: Any, /
) -> TypeGuard[Mapping[str, Any]]:
    return isinstance(obj, Mapping) and is_iterable_of(obj, str)


@dataclass(kw_only=True, slots=True)
class YieldStructSeriesElementsError(Exception):
    series: Series


@dataclass(kw_only=True, slots=True)
class _YieldStructSeriesElementsDTypeError(YieldStructSeriesElementsError):
    @override
    def __str__(self) -> str:
        return f"Series must have Struct-dtype; got {self.series.dtype}"


@dataclass(kw_only=True, slots=True)
class _YieldStructSeriesElementsNullElementsError(YieldStructSeriesElementsError):
    @override
    def __str__(self) -> str:
        return f"Series must not have nulls; got {self.series}"


##


@overload
def yield_struct_series_dataclasses(
    series: Series,
    cls: type[_TDataclass],
    /,
    *,
    forward_references: dict[str, Any] | None = ...,
    check_types: bool = ...,
    strict: Literal[True],
) -> Iterator[_TDataclass]: ...
@overload
def yield_struct_series_dataclasses(
    series: Series,
    cls: type[_TDataclass],
    /,
    *,
    forward_references: dict[str, Any] | None = ...,
    check_types: bool = ...,
    strict: bool = False,
) -> Iterator[_TDataclass | None]: ...
def yield_struct_series_dataclasses(
    series: Series,
    cls: type[_TDataclass],
    /,
    *,
    forward_references: dict[str, Any] | None = None,
    check_types: bool = True,
    strict: bool = False,
) -> Iterator[_TDataclass | None]:
    """Yield the elements of a struct-dtype Series as dataclasses."""
    from dacite import Config, from_dict

    config = Config(
        forward_references=forward_references, check_types=check_types, strict=True
    )
    for value in yield_struct_series_elements(series, strict=strict):
        yield None if value is None else from_dict(cls, value, config=config)


##


def zoned_datetime(
    *, time_unit: TimeUnit = "us", time_zone: ZoneInfoLike | timezone = UTC
) -> Datetime:
    """Create a zoned datetime data type."""
    return Datetime(time_unit=time_unit, time_zone=get_time_zone_name(time_zone))


__all__ = [
    "CheckPolarsDataFrameError",
    "ColumnsToDictError",
    "DataClassToDataFrameError",
    "DatetimeHongKong",
    "DatetimeTokyo",
    "DatetimeUSCentral",
    "DatetimeUSEastern",
    "DatetimeUTC",
    "DropNullStructSeriesError",
    "GetDataTypeOrSeriesTimeZoneError",
    "IsNullStructSeriesError",
    "RollingParametersError",
    "RollingParametersExponential",
    "RollingParametersSimple",
    "SetFirstRowAsColumnsError",
    "StructFromDataClassError",
    "YieldRowsAsDataClassesError",
    "YieldStructSeriesElementsError",
    "append_dataclass",
    "are_frames_equal",
    "ceil_datetime",
    "check_polars_dataframe",
    "collect_series",
    "columns_to_dict",
    "convert_time_zone",
    "dataclass_to_dataframe",
    "dataclass_to_schema",
    "drop_null_struct_series",
    "ensure_expr_or_series",
    "floor_datetime",
    "get_data_type_or_series_time_zone",
    "is_not_null_struct_series",
    "is_null_struct_series",
    "join",
    "map_over_columns",
    "nan_sum_agg",
    "nan_sum_cols",
    "replace_time_zone",
    "rolling_parameters",
    "set_first_row_as_columns",
    "struct_dtype",
    "struct_from_dataclass",
    "unique_element",
    "yield_rows_as_dataclasses",
    "yield_struct_series_dataclasses",
    "yield_struct_series_elements",
    "zoned_datetime",
]
