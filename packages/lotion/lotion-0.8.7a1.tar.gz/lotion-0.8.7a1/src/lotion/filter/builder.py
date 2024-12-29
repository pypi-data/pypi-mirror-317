from dataclasses import dataclass
from typing import Any

from .condition.cond import Cond
from .condition.prop import Prop
from .condition_ruleset import ConditionRuleset


@dataclass(frozen=True)
class Builder:
    conditions: list[dict]

    @staticmethod
    def create() -> "Builder":
        return Builder(conditions=[])

    def add(
        self, prop_type: Prop, prop_name: str, cond_type: Cond, value: Any = None
    ) -> "Builder":
        if prop_type == Prop.CREATED_TIME:
            raise ValueError(f"You use add_created_at() method for {prop_type}")
        if prop_type == Prop.LAST_EDITED_TIME:
            raise ValueError(f"You use add_last_edited_at() method for {prop_type}")

        ConditionRuleset(prop_type, cond_type, value).validate()
        param = {
            "property": prop_name,
            prop_type.value: {
                cond_type.value: value if value is not None else {},
            },
        }
        return Builder(conditions=[*self.conditions, param])

    def add_filter_param(self, param: dict) -> "Builder":
        return Builder(conditions=[*self.conditions, param])

    def add_created_at(self, cond_type: Cond, value: Any) -> "Builder":
        return self._add_timestamp(Prop.CREATED_TIME, cond_type, value)

    def add_last_edited_at(self, cond_type: Cond, value: Any) -> "Builder":
        return self._add_timestamp(Prop.LAST_EDITED_TIME, cond_type, value)

    def _add_timestamp(self, prop_type: Prop, cond_type: Cond, value: Any) -> "Builder":
        ConditionRuleset(prop_type, cond_type, value).validate()
        param = {
            "timestamp": prop_type.value,
            prop_type.value: {
                cond_type.value: value,
            },
        }
        return Builder(conditions=[*self.conditions, param])

    def is_empty(self) -> bool:
        return len(self.conditions) == 0

    def build(self, mode: str = "and") -> dict:
        """
        :param mode: "and" or "or"

        """
        if len(self.conditions) == 0:
            raise ValueError("Filter is empty")
        if len(self.conditions) == 1:
            return self.conditions[0]
        return {
            mode: self.conditions,
        }
