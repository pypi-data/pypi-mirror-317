import re
from dataclasses import dataclass
from types import NoneType
from typing import Any

from ..page.page_id import PageId
from .condition.cond import Cond
from .condition.prop import Prop

RULESET: dict[Prop, dict[Cond, list[type]]] = {}
RULESET[Prop.RICH_TEXT] = {
    Cond.EQUALS: [str],
    Cond.DOES_NOT_EQUAL: [str],
    Cond.CONTAINS: [str],
    Cond.DOES_NOT_CONTAIN: [str],
    Cond.IS_EMPTY: [bool],
    Cond.IS_NOT_EMPTY: [bool],
    Cond.STARTS_WITH: [str],
    Cond.ENDS_WITH: [str],
}
RULESET[Prop.CHECKBOX] = {
    Cond.EQUALS: [bool],
    Cond.DOES_NOT_EQUAL: [bool],
}
RULESET[Prop.DATE] = {
    Cond.EQUALS: [str],
    Cond.AFTER: [str],
    Cond.ON_OR_AFTER: [str],
    Cond.BEFORE: [str],
    Cond.ON_OR_BEFORE: [str],
    Cond.IS_EMPTY: [bool],
    Cond.IS_NOT_EMPTY: [bool],
    Cond.NEXT_WEEK: [NoneType],
    Cond.NEXT_MONTH: [NoneType],
    Cond.NEXT_YEAR: [NoneType],
    Cond.PAST_WEEK: [NoneType],
    Cond.PAST_MONTH: [NoneType],
    Cond.PAST_YEAR: [NoneType],
    Cond.THIS_WEEK: [NoneType],
}
RULESET[Prop.FILES] = {
    Cond.IS_EMPTY: [bool],
    Cond.IS_NOT_EMPTY: [bool],
}
RULESET[Prop.MULTI_SELECT] = {
    Cond.CONTAINS: [str],
    Cond.DOES_NOT_CONTAIN: [str],
    Cond.IS_EMPTY: [bool],
    Cond.IS_NOT_EMPTY: [bool],
}
RULESET[Prop.NUMBER] = {
    Cond.EQUALS: [int, float],
    Cond.DOES_NOT_EQUAL: [int, float],
    Cond.GREATER_THAN: [int, float],
    Cond.LESS_THAN: [int, float],
    Cond.GREATER_THAN_OR_EQUAL_TO: [int, float],
    Cond.LESS_THAN_OR_EQUAL_TO: [int, float],
    Cond.IS_EMPTY: [bool],
    Cond.IS_NOT_EMPTY: [bool],
}
RULESET[Prop.PEOPLE] = {
    Cond.CONTAINS: [str],
    Cond.DOES_NOT_CONTAIN: [str],
    Cond.IS_EMPTY: [bool],
    Cond.IS_NOT_EMPTY: [bool],
}
RULESET[Prop.RELATION] = {
    Cond.CONTAINS: [str],
    Cond.DOES_NOT_CONTAIN: [str],
    Cond.IS_EMPTY: [bool],
    Cond.IS_NOT_EMPTY: [bool],
}
RULESET[Prop.SELECT] = {
    Cond.EQUALS: [str],
    Cond.DOES_NOT_EQUAL: [str],
    Cond.IS_EMPTY: [bool],
    Cond.IS_NOT_EMPTY: [bool],
}
RULESET[Prop.STATUS] = {
    Cond.EQUALS: [str],
    Cond.DOES_NOT_EQUAL: [str],
    Cond.IS_EMPTY: [bool],
    Cond.IS_NOT_EMPTY: [bool],
}
RULESET[Prop.ID] = {
    Cond.EQUALS: [int],
    Cond.DOES_NOT_EQUAL: [int],
    Cond.GREATER_THAN: [int],
    Cond.LESS_THAN: [int],
    Cond.GREATER_THAN_OR_EQUAL_TO: [int],
    Cond.LESS_THAN_OR_EQUAL_TO: [int],
    Cond.IS_EMPTY: [bool],
    Cond.IS_NOT_EMPTY: [bool],
}
RULESET[Prop.CREATED_TIME] = {
    Cond.EQUALS: [str],
    Cond.AFTER: [str],
    Cond.ON_OR_AFTER: [str],
    Cond.BEFORE: [str],
    Cond.ON_OR_BEFORE: [str],
    Cond.IS_EMPTY: [bool],
    Cond.IS_NOT_EMPTY: [bool],
    Cond.NEXT_WEEK: [NoneType],
    Cond.NEXT_MONTH: [NoneType],
    Cond.NEXT_YEAR: [NoneType],
    Cond.PAST_WEEK: [NoneType],
    Cond.PAST_MONTH: [NoneType],
    Cond.PAST_YEAR: [NoneType],
    Cond.THIS_WEEK: [NoneType],
}
RULESET[Prop.LAST_EDITED_TIME] = {
    Cond.EQUALS: [str],
    Cond.AFTER: [str],
    Cond.ON_OR_AFTER: [str],
    Cond.BEFORE: [str],
    Cond.ON_OR_BEFORE: [str],
    Cond.IS_EMPTY: [bool],
    Cond.IS_NOT_EMPTY: [bool],
    Cond.NEXT_WEEK: [NoneType],
    Cond.NEXT_MONTH: [NoneType],
    Cond.NEXT_YEAR: [NoneType],
    Cond.PAST_WEEK: [NoneType],
    Cond.PAST_MONTH: [NoneType],
    Cond.PAST_YEAR: [NoneType],
    Cond.THIS_WEEK: [NoneType],
}


@dataclass(frozen=True)
class ConditionRuleset:
    prop: Prop
    cond: Cond
    value: Any

    def validate(self) -> None:
        # 必須のチェック
        self.validate_prop()
        self.validate_cond()
        self.validate_value()

        # オプションのチェック
        self.validate_page_id()
        self.validate_date()

    def validate_prop(self) -> None:
        if self.prop not in RULESET:
            raise ValueError(f"Property {self.prop} is not supported")

    def validate_cond(self) -> None:
        if self.cond not in RULESET[self.prop]:
            msg = f"Condition {self.cond} is not supported for property {self.prop}"
            raise ValueError(msg)

    def validate_value(self) -> None:
        if type(self.value) not in RULESET[self.prop][self.cond]:
            msg = f"Value type {type(self.value)} is not supported for property {self.prop} with condition {self.cond}"
            raise ValueError(msg)

    def validate_page_id(self) -> None:
        if self.prop not in [Prop.PEOPLE, Prop.RELATION]:
            return
        if self.cond not in [Cond.CONTAINS, Cond.DOES_NOT_CONTAIN]:
            return
        # ユーザもしくはリレーションの場合は、ページIDに変換できるかどうかを確認する
        PageId(self.value)

    def validate_date(self) -> None:
        if self.prop != Prop.DATE:
            return
        if self.cond not in [
            Cond.AFTER,
            Cond.ON_OR_AFTER,
            Cond.BEFORE,
            Cond.ON_OR_BEFORE,
        ]:
            return
        # "2021-05-10"、"2021-05-10T12:00:00"、"2021-10-15T12:00:00-07:00"
        # のような形式であるかどうかを正規表現で確認する
        if re.match(r"\d{4}-\d{2}-\d{2}", self.value):
            return
        if re.match(r"\d{4}-\d{2}-\d{2}T?\d{2}:\d{2}:\d{2}", self.value):
            return
        if re.match(r"\d{4}-\d{2}-\d{2}T?\d{2}:\d{2}:\d{2}[-+]?\d{2}:\d{2}", self.value):
            return
        raise ValueError(f"Date value {self.value} is invalid")
