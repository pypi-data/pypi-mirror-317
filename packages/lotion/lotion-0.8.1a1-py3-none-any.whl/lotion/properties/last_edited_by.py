from dataclasses import dataclass
from typing import Any, Type, TypeVar

from .property import Property

T = TypeVar("T", bound="LastEditedBy")


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

    @classmethod
    def of(cls: Type[T], key: str, param: dict) -> T:
        return cls(id=param["id"], name=key, last_edited_by=param["last_edited_by"])

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
