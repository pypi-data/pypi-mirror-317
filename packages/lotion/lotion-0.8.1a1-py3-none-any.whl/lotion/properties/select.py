from dataclasses import dataclass
from typing import Type, TypeVar

from .property import Property

T = TypeVar("T", bound="Select")


@dataclass
class Select(Property):
    selected_name: str
    selected_id: str | None
    selected_color: str | None
    type: str = "select"

    def __init__(
        self,
        name: str,
        selected_name: str = "",
        selected_id: str | None = None,
        selected_color: str | None = None,
        id: str | None = None,
    ):
        self.name = name
        self.id = id
        self.selected_name = selected_name
        self.selected_id = selected_id
        self.selected_color = selected_color

    @classmethod
    def of(cls: Type[T], name: str, param: dict) -> T:
        select = param["select"]
        if select is None:
            return cls(name=name)
        return cls(
            name=name,
            selected_id=select["id"],
            selected_name=select["name"],
            selected_color=select["color"],
            id=param["id"],
        )

    @classmethod
    def empty(cls: Type[T], name: str | None = None) -> T:
        return cls(name=name or cls.PROP_NAME)

    def is_empty(self) -> bool:
        return self.selected_name == ""

    def __dict__(self):
        if self.selected_id is None:
            return {
                self.name: {
                    "type": self.type,
                    "select": None,
                }
            }
        result = {
            "type": self.type,
            "select": {
                "id": self.selected_id,
                "name": self.selected_name,
                "color": self.selected_color,
            },
        }
        if self.id is not None:
            result["id"] = self.id
        return {self.name: result}

    def value_for_filter(self) -> str:
        return self.selected_name if self.selected_name is not None else ""

    # __hash__と__eq__を実装することで、リストやセットの中で比較が可能になる
    def __hash__(self):
        return hash(self.selected_id)

    def __eq__(self, other):
        return self.selected_id == other.selected_id


@dataclass(frozen=True)
class Selects:
    values: list[Select]

    def get(self, status_name: str) -> Select:
        for value in self.values:
            if value.selected_name == status_name:
                return value
        raise ValueError(f"Select not found: {status_name}")

    @property
    def size(self) -> int:
        return len(self.values)
