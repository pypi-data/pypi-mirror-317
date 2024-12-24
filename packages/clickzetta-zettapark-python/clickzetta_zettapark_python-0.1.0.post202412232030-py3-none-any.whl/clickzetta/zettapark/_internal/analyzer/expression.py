#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
# Copyright (c) 2023-2024 Yunqi Inc. All rights reserved.
#

import copy
import uuid
from functools import cached_property
from typing import TYPE_CHECKING, AbstractSet, Any, List, Optional, Tuple

import clickzetta.zettapark._internal.utils

if TYPE_CHECKING:
    from clickzetta.zettapark._internal.analyzer.query_plan import (
        QueryPlan,
    )  # pragma: no cover

from clickzetta.zettapark._internal.error_message import (
    ZettaparkClientExceptionMessages,
)
from clickzetta.zettapark._internal.type_utils import (
    VALID_PYTHON_TYPES_FOR_LITERAL_VALUE,
    VALID_ZETTAPARK_TYPES_FOR_LITERAL_VALUE,
    infer_type,
)
from clickzetta.zettapark.types import DataType

COLUMN_DEPENDENCY_DOLLAR = frozenset(
    "$"
)  # depend on any columns with expression `$n`. We don't flatten when seeing a $
COLUMN_DEPENDENCY_ALL = None  # depend on all columns including subquery's and same level columns when we can't infer the dependent columns
COLUMN_DEPENDENCY_EMPTY: AbstractSet[str] = frozenset()  # depend on no columns.


def derive_dependent_columns(
    *expressions: "Optional[Expression]",
) -> Optional[AbstractSet[str]]:
    result = set()
    for exp in expressions:
        if exp is not None:
            child_dependency = exp.dependent_column_names()
            if child_dependency == COLUMN_DEPENDENCY_DOLLAR:
                return COLUMN_DEPENDENCY_DOLLAR
            if child_dependency == COLUMN_DEPENDENCY_ALL:
                return COLUMN_DEPENDENCY_ALL
            assert child_dependency is not None
            result.update(child_dependency)
    return result


class Expression:
    """Consider removing attributes, and adding properties and methods.
    A subclass of Expression may have no child, one child, or multiple children.
    But the constructor accepts a single child. This might be refactored in the future.
    """

    def __init__(self, child: Optional["Expression"] = None) -> None:
        """
        Subclasses will override these attributes
        """
        self.child = child
        self.nullable = True
        self.children = [child] if child else None
        self.datatype: Optional[DataType] = None

    def dependent_column_names(self) -> Optional[AbstractSet[str]]:
        # TODO: consider adding it to __init__ or use cached_property.
        return COLUMN_DEPENDENCY_EMPTY

    @property
    def pretty_name(self) -> str:
        """Returns a user-facing string representation of this expression's name.
        This should usually match the name of the function in SQL."""
        return self.__class__.__name__.upper()

    @property
    def sql(self) -> str:
        """The only place that uses Expression.sql() to generate sql statement
        is relational_grouped_dataframe.py's __toDF(). Re-consider whether we need to make the sql generation
        consistent among all different Expressions.
        """
        children_sql = (
            ", ".join([x.sql for x in self.children]) if self.children else ""
        )
        return f"{self.pretty_name}({children_sql})"

    @property
    def column_name(self) -> str:
        return self.sql

    def __str__(self) -> str:
        return self.pretty_name


class NamedExpression:
    name: str
    _expr_id: Optional[uuid.UUID] = None

    @property
    def expr_id(self) -> uuid.UUID:
        if not self._expr_id:
            self._expr_id = uuid.uuid4()
        return self._expr_id

    def __copy__(self):
        new = copy.copy(super())
        new._expr_id = None  # type: ignore
        return new


class ScalarSubquery(Expression):
    def __init__(self, plan: "QueryPlan") -> None:
        super().__init__()
        self.plan = plan

    def dependent_column_names(self) -> Optional[AbstractSet[str]]:
        return COLUMN_DEPENDENCY_DOLLAR


class MultipleExpression(Expression):
    def __init__(self, expressions: List[Expression]) -> None:
        super().__init__()
        self.expressions = expressions

    def dependent_column_names(self) -> Optional[AbstractSet[str]]:
        return derive_dependent_columns(*self.expressions)


class InExpression(Expression):
    def __init__(
        self, columns: Expression, values: List[Expression], positive: bool
    ) -> None:
        super().__init__()
        self.columns = columns
        self.values = values
        self.positive = positive

    def dependent_column_names(self) -> Optional[AbstractSet[str]]:
        return derive_dependent_columns(self.columns, *self.values)


class Attribute(Expression, NamedExpression):
    def __init__(self, name: str, datatype: DataType, nullable: bool = True) -> None:
        super().__init__()
        self.name = name
        self.datatype: DataType = datatype
        self.nullable = nullable

    def with_name(self, new_name: str) -> "Attribute":
        if self.name == new_name:
            return self
        else:
            return Attribute(
                clickzetta.zettapark._internal.utils.quote_name(new_name),
                self.datatype,
                self.nullable,
            )

    @property
    def sql(self) -> str:
        return self.name

    def __str__(self):
        return self.name

    def dependent_column_names(self) -> Optional[AbstractSet[str]]:
        return {self.name}


class Star(Expression):
    def __init__(
        self, expressions: List[Attribute], df_alias: Optional[str] = None
    ) -> None:
        super().__init__()
        self.expressions = expressions
        self.df_alias = df_alias

    def dependent_column_names(self) -> Optional[AbstractSet[str]]:
        return derive_dependent_columns(*self.expressions)


class UnresolvedAttribute(Expression, NamedExpression):
    def __init__(
        self, name: str, is_sql_text: bool = False, df_alias: Optional[str] = None
    ) -> None:
        super().__init__()
        self.df_alias = df_alias
        self.name = name
        self.is_sql_text = is_sql_text
        if "$" in name:
            # $n refers to a column by index. We don't consider column index yet.
            # even though "$" isn't necessarily used to refer to a column by index. We're conservative here.
            self._dependent_column_names = COLUMN_DEPENDENCY_DOLLAR
        else:
            self._dependent_column_names = (
                COLUMN_DEPENDENCY_ALL if is_sql_text else {name}
            )

    @property
    def sql(self) -> str:
        return self.name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return type(other) is type(self) and other.name == self.name

    def __hash__(self):
        return hash(self.name)

    def dependent_column_names(self) -> Optional[AbstractSet[str]]:
        return self._dependent_column_names


class Literal(Expression):
    def __init__(
        self,
        value: Any,
        datatype: Optional[DataType] = None,
        identity: Optional[bool] = None,
    ) -> None:
        super().__init__()

        # check value
        if not isinstance(value, VALID_PYTHON_TYPES_FOR_LITERAL_VALUE):
            raise ZettaparkClientExceptionMessages.PLAN_CANNOT_CREATE_LITERAL(
                type(value)
            )
        self.value = value
        self.identity = identity

        self.datatype: DataType
        # check datatype
        if datatype:
            if not isinstance(datatype, VALID_ZETTAPARK_TYPES_FOR_LITERAL_VALUE):
                raise ZettaparkClientExceptionMessages.PLAN_CANNOT_CREATE_LITERAL(
                    str(datatype)
                )
            self.datatype = datatype
        else:
            self.datatype = infer_type(value)

    @cached_property
    def column_name(self) -> str:
        if type(self.value) is str:
            return f"'{self.value}'"
        # TODO: support other kinds of literal values
        return str(self.value)


class Interval(Expression):
    def __init__(
        self,
        year: Optional[int] = None,
        month: Optional[int] = None,
        week: Optional[int] = None,
        day: Optional[int] = None,
        hour: Optional[int] = None,
        minute: Optional[int] = None,
        second: Optional[int] = None,
        millisecond: Optional[int] = None,
        microsecond: Optional[int] = None,
    ) -> None:
        super().__init__()
        self._year_month: List[Tuple[str, int]] = []
        self._day_time: List[Tuple[str, int]] = []
        if year is not None:
            self._year_month.append(("YEAR", year))
        if month is not None:
            self._year_month.append(("MONTH", month))
        if week is not None:
            self._year_month.append(("WEEK", week))
        if day is not None:
            self._day_time.append(("DAY", day))
        if hour is not None:
            self._day_time.append(("HOUR", hour))
        if minute is not None:
            self._day_time.append(("MINUTE", minute))
        if second is not None:
            self._day_time.append(("SECOND", second))
        if millisecond is not None:
            self._day_time.append(("MILLISECOND", millisecond))
        if microsecond is not None:
            self._day_time.append(("MICROSECOND", microsecond))

    @property
    def sql(self) -> str:
        year_month = " ".join(f"{v} {u}" for u, v in self._year_month)
        day_time = " ".join(f"{v} {u}" for u, v in self._day_time)
        return f"INTERVAL '{year_month}' + INTERVAL '{day_time}'"

    def __str__(self) -> str:
        return self.sql


class Like(Expression):
    def __init__(self, expr: Expression, pattern: Expression) -> None:
        super().__init__(expr)
        self.expr = expr
        self.pattern = pattern

    def dependent_column_names(self) -> Optional[AbstractSet[str]]:
        return derive_dependent_columns(self.expr, self.pattern)


class RegExp(Expression):
    def __init__(self, expr: Expression, pattern: Expression) -> None:
        super().__init__(expr)
        self.expr = expr
        self.pattern = pattern

    def dependent_column_names(self) -> Optional[AbstractSet[str]]:
        return derive_dependent_columns(self.expr, self.pattern)


class Collate(Expression):
    def __init__(self, expr: Expression, collation_spec: str) -> None:
        super().__init__(expr)
        self.expr = expr
        self.collation_spec = collation_spec

    def dependent_column_names(self) -> Optional[AbstractSet[str]]:
        return derive_dependent_columns(self.expr)


class SubfieldString(Expression):
    def __init__(self, expr: Expression, field: str) -> None:
        super().__init__(expr)
        self.expr = expr
        self.field = field

    def dependent_column_names(self) -> Optional[AbstractSet[str]]:
        return derive_dependent_columns(self.expr)


class SubfieldInt(Expression):
    def __init__(self, expr: Expression, field: int) -> None:
        super().__init__(expr)
        self.expr = expr
        self.field = field

    def dependent_column_names(self) -> Optional[AbstractSet[str]]:
        return derive_dependent_columns(self.expr)


class FunctionExpression(Expression):
    def __init__(
        self,
        name: str,
        arguments: List[Expression],
        is_distinct: bool,
        api_call_source: Optional[str] = None,
        *,
        is_data_generator: bool = False,
    ) -> None:
        super().__init__()
        self.name = name
        self.children = arguments
        self.is_distinct = is_distinct
        self.api_call_source = api_call_source
        self.is_data_generator = is_data_generator

    @property
    def pretty_name(self) -> str:
        return self.name

    @property
    def sql(self) -> str:
        return self._to_column_name(parse_local_name=False)

    @property
    def column_name(self) -> str:
        return self._to_column_name(parse_local_name=True)

    def _to_column_name(self, parse_local_name: bool) -> str:
        from clickzetta.zettapark._internal.analyzer.analyzer_utils import (
            function_expression,
        )

        return function_expression(
            self.name,
            [c.sql for c in self.children],
            self.is_distinct,
            parse_local_name,
        )

    def dependent_column_names(self) -> Optional[AbstractSet[str]]:
        return derive_dependent_columns(*self.children)


class WithinGroup(Expression):
    def __init__(self, expr: Expression, order_by_cols: List[Expression]) -> None:
        super().__init__(expr)
        self.expr = expr
        self.order_by_cols = order_by_cols
        self.datatype = expr.datatype

    def dependent_column_names(self) -> Optional[AbstractSet[str]]:
        return derive_dependent_columns(self.expr, *self.order_by_cols)


class CaseWhen(Expression):
    def __init__(
        self,
        branches: List[Tuple[Expression, Expression]],
        else_value: Optional[Expression] = None,
    ) -> None:
        super().__init__()
        self.branches = branches
        self.else_value = else_value

    def dependent_column_names(self) -> Optional[AbstractSet[str]]:
        exps = []
        for exp_tuple in self.branches:
            exps.extend(exp_tuple)
        if self.else_value is not None:
            exps.append(self.else_value)
        return derive_dependent_columns(*exps)


class UDF(Expression):
    def __init__(
        self,
        udf_name: str,
        children: List[Expression],
        datatype: DataType,
        nullable: bool = True,
        api_call_source: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.udf_name = udf_name
        self.children = children
        self.datatype = datatype
        self.nullable = nullable
        self.api_call_source = api_call_source

    def dependent_column_names(self) -> Optional[AbstractSet[str]]:
        return derive_dependent_columns(*self.children)


class ListAgg(Expression):
    def __init__(self, col: Expression, delimiter: str, is_distinct: bool) -> None:
        super().__init__()
        self.col = col
        self.delimiter = delimiter
        self.is_distinct = is_distinct

    def dependent_column_names(self) -> Optional[AbstractSet[str]]:
        return derive_dependent_columns(self.col)
