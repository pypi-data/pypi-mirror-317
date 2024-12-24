#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
# Copyright (c) 2023-2024 Yunqi Inc. All rights reserved.
#

from typing import List, Optional

from clickzetta.zettapark._internal.analyzer.expression import Expression
from clickzetta.zettapark._internal.analyzer.query_plan_node import LogicalPlan
from clickzetta.zettapark._internal.error_message import (
    ZettaparkClientExceptionMessages,
)

SUPPORTED_JOIN_TYPE_STR = [
    "inner",
    "outer",
    "full",
    "fullouter",
    "leftouter",
    "left",
    "rightouter",
    "right",
    "leftsemi",
    "semi",
    "leftanti",
    "anti",
    "cross",
    "asof",
]


def create_join_type(join_type: str) -> "JoinType":
    jt = join_type.strip().lower().replace("_", "")

    if jt == "inner":
        return Inner()

    if jt in ["outer", "full", "fullouter"]:
        return FullOuter()

    if jt in ["leftouter", "left"]:
        return LeftOuter()

    if jt in ["rightouter", "right"]:
        return RightOuter()

    if jt in ["leftsemi", "semi"]:
        return LeftSemi()

    if jt in ["leftanti", "anti"]:
        return LeftAnti()

    if jt == "cross":
        return Cross()

    if jt == "asof":
        return AsOf()

    raise ZettaparkClientExceptionMessages.DF_JOIN_INVALID_JOIN_TYPE(
        join_type, ", ".join(SUPPORTED_JOIN_TYPE_STR)
    )


class BinaryNode(LogicalPlan):
    sql: str

    def __init__(self, left: LogicalPlan, right: LogicalPlan) -> None:
        super().__init__()
        self.left = left
        self.right = right
        self.children = [self.left, self.right]


class SetOperation(BinaryNode):
    pass


class Except(SetOperation):
    sql = "EXCEPT"


class Intersect(SetOperation):
    sql = "INTERSECT"


class Union(SetOperation):
    def __init__(self, left: LogicalPlan, right: LogicalPlan, is_all: bool) -> None:
        super().__init__(left, right)
        self.is_all = is_all

    @property
    def sql(self) -> str:
        return f"UNION{' ALL' if self.is_all else ''}"


class JoinType:
    sql: str


class InnerLike(JoinType):
    pass


class Inner(InnerLike):
    sql = "INNER"


class Cross(InnerLike):
    sql = "CROSS"


class LeftOuter(JoinType):
    sql = "LEFT OUTER"


class RightOuter(JoinType):
    sql = "RIGHT OUTER"


class FullOuter(JoinType):
    sql = "FULL OUTER"


class LeftSemi(JoinType):
    sql = "LEFT SEMI"


class LeftAnti(JoinType):
    sql = "LEFT ANTI"


class AsOf(JoinType):
    sql = "ASOF"


class NaturalJoin(JoinType):
    def __init__(self, tpe: JoinType) -> None:
        if not isinstance(
            tpe,
            (
                Inner,
                LeftOuter,
                RightOuter,
                FullOuter,
            ),
        ):
            raise ZettaparkClientExceptionMessages.DF_JOIN_INVALID_NATURAL_JOIN_TYPE(
                tpe.__class__.__name__
            )
        self.sql = "NATURAL " + tpe.sql
        self.tpe = tpe


class UsingJoin(JoinType):
    def __init__(self, tpe: JoinType, using_columns: List[str]) -> None:
        if not isinstance(
            tpe,
            (
                Inner,
                LeftOuter,
                LeftSemi,
                RightOuter,
                FullOuter,
                LeftAnti,
                AsOf,
            ),
        ):
            raise ZettaparkClientExceptionMessages.DF_JOIN_INVALID_USING_JOIN_TYPE(
                tpe.__class__.__name__
            )
        self.sql = "USING " + tpe.sql
        self.tpe = tpe
        self.using_columns = using_columns


class Join(BinaryNode):
    def __init__(
        self,
        left: LogicalPlan,
        right: LogicalPlan,
        join_type: JoinType,
        join_condition: Optional["Expression"],
        match_condition: Optional["Expression"],
    ) -> None:
        super().__init__(left, right)
        self.join_type = join_type
        self.join_condition = join_condition
        self.match_condition = match_condition

    @property
    def sql(self) -> str:
        return self.join_type.sql
