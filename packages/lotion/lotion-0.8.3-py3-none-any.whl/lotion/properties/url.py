from dataclasses import dataclass
from typing import Type, TypeVar

from .property import Property

T = TypeVar("T", bound="Url")


@dataclass
class Url(Property):
    url: str = ""

    PROP_NAME = "url"  # 自分で使うために準備。本来は不要。

    def __init__(self, name: str, url: str = "", id: str | None = None):
        self.name = name
        self.url = url
        self.id = id

    @classmethod
    def of(cls: Type[T], name: str, param: dict) -> T:
        url = param["url"] if param.get("url") else ""
        return cls(
            name=name,
            url=url,
            id=param["id"],
        )

    @classmethod
    def from_url(cls: Type[T], url: str, name: str | None = None) -> T:
        return cls(
            name=name or cls.PROP_NAME,
            url=url,
        )

    @classmethod
    def empty(cls: Type[T], name: str | None = None) -> T:
        return cls(name=name or cls.PROP_NAME)

    @property
    def type(self) -> str:
        return "url"

    def value_for_filter(self) -> str:
        return self.url

    def __dict__(self):
        result = {
            "type": self.type,
            "url": self.url if self.url != "" else None,
        }
        if self.id is not None:
            result["id"] = self.id
        return {
            self.name: result,
        }
