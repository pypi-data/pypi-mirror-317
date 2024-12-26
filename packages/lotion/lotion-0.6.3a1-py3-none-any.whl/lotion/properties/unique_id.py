from dataclasses import dataclass
from typing import Any

from .property import Property


@dataclass
class UniqueId(Property):
    """UniqueId class

    ex.
    {'id': 'vI%3FY', 'type': 'unique_id', 'unique_id': {'prefix': None, 'number': 1}}
    """

    prefix: str | None
    number: int

    def __init__(
        self,
        name: str,
        number: int,
        id: str,
        prefix: str | None = None,
    ) -> None:
        self.name = name
        self.prefix = prefix
        self.number = number
        self.id = id

    @staticmethod
    def of(key: str, param: dict) -> "UniqueId":
        return UniqueId(
            id=param["id"],
            name=key,
            prefix=param["unique_id"]["prefix"],
            number=param["unique_id"]["number"],
        )

    @property
    def type(self) -> str:
        return "unique_id"

    def __dict__(self) -> dict:
        raise NotImplementedError("this dict method must not be called")

    def value_for_filter(self) -> Any:
        return self.number
