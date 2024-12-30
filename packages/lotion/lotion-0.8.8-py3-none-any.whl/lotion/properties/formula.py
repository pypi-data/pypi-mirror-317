from dataclasses import dataclass
from typing import Type, TypeVar

from .property import Property

T = TypeVar("T", bound="Formula")


@dataclass
class Formula(Property):
    """Formula class

    ex.
    {'id': 'h_pG', 'type': 'formula', 'formula': {'type': 'number', 'number': 50}}
    """

    _formula: dict

    def __init__(
        self,
        name: str,
        formula: dict = {},
        id: str | None = None,  # noqa: A002
    ) -> None:
        self.name = name
        self._formula = formula
        self.id = id

    @classmethod
    def of(cls: Type[T], key: str, param: dict) -> T:
        return cls(
            id=param["id"],
            name=key,
            formula=param["formula"],
        )

    @property
    def value(self) -> dict:
        formula_type = self._formula["type"]
        return self._formula[formula_type]

    @property
    def type(self) -> str:
        return "formula"

    def __dict__(self) -> dict:
        raise NotImplementedError("this dict method must not be called")

    def value_for_filter(self) -> str:
        raise NotImplementedError
