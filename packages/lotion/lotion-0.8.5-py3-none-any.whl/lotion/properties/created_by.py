from dataclasses import dataclass
from typing import Any, Type, TypeVar

from .property import Property

T = TypeVar("T", bound="CreatedBy")


@dataclass
class CreatedBy(Property):
    def __init__(
        self,
        name: str,
        created_by_param: dict,
        id: str | None = None,  # noqa: A002
    ) -> None:
        self.name = name
        self.created_by_param = created_by_param
        self.id = id

    @classmethod
    def of(cls: Type[T], key: str, param: dict) -> T:
        return cls(id=param["id"], name=key, created_by_param=param["created_by"])

    def __dict__(self) -> dict[str, Any]:
        return {
            self.name: {
                "id": self.id,
                "type": self.type,
                "created_by": self.created_by_param,
            },
        }

    @property
    def type(self) -> str:
        return "created_by"  # NOTE: created_timeではなくdateにする

    def value_for_filter(self) -> str:
        raise NotImplementedError()
