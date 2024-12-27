from dataclasses import dataclass
from datetime import datetime
from typing import Any, Type, TypeVar

from .property import Property
from ..datetime_utils import convert_to_date_or_datetime

T = TypeVar("T", bound="CreatedTime")


@dataclass
class CreatedTime(Property):
    def __init__(
        self,
        name: str,
        value: datetime,
        id: str | None = None,  # noqa: A002
    ) -> None:
        self.name = name
        self.value = value
        self.id = id

    @classmethod
    def create(cls: Type[T], key, value: str) -> T:
        return cls(
            name=key,
            value=convert_to_date_or_datetime(value),
        )

    def __dict__(self) -> dict[str, Any]:
        _date = {
            "start": self.value.isoformat(),
            "end": None,
            "time_zone": None,
        }
        return {
            self.name: {
                "type": self.type,
                "date": _date,
            },
        }

    @property
    def type(self) -> str:
        return "date"  # NOTE: created_timeではなくdateにする

    def value_for_filter(self) -> str:
        return self.value.isoformat()
