from dataclasses import dataclass

from .property import Property


@dataclass
class Checkbox(Property):
    checked: bool
    type: str = "checkbox"

    def __init__(
        self, name: str, checked: bool, id: str | None = None
    ) -> None:  # noqa: A002, FBT001
        self.name = name
        self.checked = checked or False
        self.id = id

    @staticmethod
    def of(name: str, param: dict) -> "Checkbox":
        return Checkbox(
            name=name,
            checked=param["checkbox"],
            id=param["id"],
        )

    @staticmethod
    def true(name: str) -> "Checkbox":
        return Checkbox(
            name=name,
            checked=True,
        )

    @staticmethod
    def false(name: str) -> "Checkbox":
        return Checkbox(
            name=name,
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
