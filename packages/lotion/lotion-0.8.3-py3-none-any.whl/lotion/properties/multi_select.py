from dataclasses import dataclass
from typing import Type, TypeVar

from .property import Property

T = TypeVar("T", bound="MultiSelect")


@dataclass(frozen=True)
class MultiSelectElement:
    id: str
    name: str
    color: str | None = None
    type: str = "multi_select"

    TYPE = "multi_select"

    def __dict__(self) -> dict:
        result = {
            "id": self.id,
            "name": self.name,
        }
        if self.color:
            result["color"] = self.color
        return result

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MultiSelectElement):
            return False
        return self.id == other.id


@dataclass
class MultiSelectElements:
    values: list[MultiSelectElement]

    def get(self, multi_select_name: str | list[str]) -> list[MultiSelectElement]:
        if isinstance(multi_select_name, str):
            return [value for value in self.values if value.name == multi_select_name]
        return [value for value in self.values if value.name in multi_select_name]

    @property
    def size(self) -> int:
        return len(self.values)


@dataclass
class MultiSelect(Property):
    values: list[MultiSelectElement]
    type: str = "multi_select"

    def __init__(self, name: str, values: list[MultiSelectElement], id: str | None = None) -> None:  # noqa: A002
        self.name = name
        self.values = values
        self.id = id

    def __post_init__(self) -> None:
        if not all(isinstance(value, MultiSelectElement) for value in self.values):
            raise ValueError("All values must be MultiSelectElement instances.")

    @classmethod
    def of(cls: Type[T], name: str, param: dict) -> T:
        multi_select = [
            MultiSelectElement(
                id=element["id"],
                name=element["name"],
                color=element["color"],
            )
            for element in param["multi_select"]
        ]

        return cls(
            name=name,
            values=multi_select,
            id=param["id"],
        )

    @classmethod
    def create(cls: Type[T], values: list[dict[str, str]], name: str | None = None) -> T:
        """
        Create a MultiSelect instance from a list of dictionaries.

        Args:
            name (str): Name of the property.
            values (list[dict[str, str]]): List of dictionaries. Each dictionary should have keys "id" and "name".

        Returns:
            MultiSelect: MultiSelect instance.
        """
        multi_select = [MultiSelectElement(id=element["id"], name=element["name"]) for element in values]
        return cls(
            name=name or cls.PROP_NAME,
            values=multi_select,
        )

    @classmethod
    def from_elements(cls: Type[T], elements: list[MultiSelectElement], name: str | None = None) -> T:
        return cls(name=name or cls.PROP_NAME, values=elements)

    def __dict__(self) -> dict:
        result = {
            "type": self.type,
            "multi_select": [e.__dict__() for e in self.values],
        }
        if self.id is not None:
            result["id"] = self.id
        return {self.name: result}

    def value_for_filter(self) -> str:
        raise NotImplementedError
