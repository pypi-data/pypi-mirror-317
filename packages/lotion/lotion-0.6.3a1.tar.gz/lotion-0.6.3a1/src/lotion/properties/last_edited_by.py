from dataclasses import dataclass
from typing import Any

from .property import Property


@dataclass
class LastEditedBy(Property):
    def __init__(
        self,
        name: str,
        last_edited_by: dict,
        id: str | None = None,  # noqa: A002
    ) -> None:
        self.name = name
        self.last_edited_by = last_edited_by
        self.id = id

    @staticmethod
    def of(key: str, param: dict) -> "LastEditedBy":
        return LastEditedBy(
            id=param["id"], name=key, last_edited_by=param["last_edited_by"]
        )

    def __dict__(self) -> dict[str, Any]:
        return {
            self.name: {
                "id": self.id,
                "type": self.type,
                "last_edited_by": self.last_edited_by,
            },
        }

    @property
    def type(self) -> str:
        return "last_edited_by"  # NOTE: created_timeではなくdateにする

    def value_for_filter(self) -> str:
        raise NotImplementedError()
