from dataclasses import dataclass

from .property import Property


@dataclass
class Number(Property):
    number: int | None
    type: str = "number"

    def __init__(
        self,
        name: str,
        id: str | None = None,  # noqa: A002
        number: int | None = None,
    ) -> None:
        self.name = name
        self.id = id
        self.number = number

    def add(self, count: int) -> "Number":
        prev = self.number if self.number is not None else 0
        return Number(
            name=self.name,
            id=self.id,
            number=prev + count,
        )

    @staticmethod
    def of(name: str, param: dict) -> "Number":
        if param["number"] is None:
            return Number(name=name, id=param["id"])
        return Number(
            name=name,
            id=param["id"],
            number=param["number"],
        )

    @staticmethod
    def empty(name: str) -> "Number":
        return Number(name=name)

    def is_empty(self) -> bool:
        return self.number is None

    @property
    def value(self) -> int:
        return self.number or 0

    def __dict__(self) -> dict:
        result = {
            "type": self.type,
            self.type: self.number,
        }
        if self.id is not None:
            result["id"] = self.id
        return {
            self.name: result,
        }

    @staticmethod
    def from_num(name: str, value: int) -> "Number":
        return Number(
            name=name,
            number=value,
        )

    def value_for_filter(self):
        return self.number
