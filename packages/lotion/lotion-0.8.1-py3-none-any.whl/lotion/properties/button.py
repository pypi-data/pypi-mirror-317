from dataclasses import dataclass
from typing import Type, TypeVar

from .property import Property

T = TypeVar("T", bound="Button")


@dataclass
class Button(Property):
    id: str
    name: str
    type: str = "button"

    @classmethod
    def of(cls: Type[T], key: str, property: dict) -> T:
        return cls(id=property["id"], name=key)

    def value_for_filter(self) -> str:
        raise NotImplementedError

    def __dict__(self) -> dict:
        return {
            self.name: {
                "id": self.id,
                "type": self.type,
                "button": {},
            },
        }
