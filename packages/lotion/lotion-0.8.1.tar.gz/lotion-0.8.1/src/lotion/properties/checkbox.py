from dataclasses import dataclass
from typing import Type, TypeVar

from .property import Property

T = TypeVar("T", bound="Checkbox")


@dataclass
class Checkbox(Property):
    checked: bool
    type: str = "checkbox"
    PROP_NAME: str = "checkbox"

    def __init__(self, name: str, checked: bool, id: str | None = None) -> None:  # noqa: A002, FBT001
        self.name = name
        self.checked = checked or False
        self.id = id

    @classmethod
    def of(cls: Type[T], name: str, param: dict) -> T:
        return cls(
            name=name,
            checked=param["checkbox"],
            id=param["id"],
        )

    @classmethod
    def true(cls: Type[T], name: str | None = None) -> T:
        return cls(
            name=name or cls.PROP_NAME,
            checked=True,
        )

    @classmethod
    def false(cls: Type[T], name: str | None = None) -> T:
        return cls(
            name=name or cls.PROP_NAME,
            checked=False,
        )

    def __dict__(self) -> dict:
        result = {
            "type": self.type,
            "checkbox": self.checked,
        }
        if self.id is not None:
            result["id"] = self.id
        return {self.name: result}

    def value_for_filter(self) -> str:
        raise NotImplementedError
