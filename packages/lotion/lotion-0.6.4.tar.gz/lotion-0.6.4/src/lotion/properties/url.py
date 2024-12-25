from dataclasses import dataclass

from .property import Property


@dataclass
class Url(Property):
    url: str = ""

    def __init__(self, name: str, url: str = "", id: str | None = None):
        self.name = name
        self.url = url
        self.id = id

    @staticmethod
    def of(name: str, param: dict) -> "Url":
        url = param["url"] if param.get("url") else ""
        return Url(
            name=name,
            url=url,
            id=param["id"],
        )

    @staticmethod
    def from_url(url: str, name: str = "URL") -> "Url":
        return Url(
            name=name,
            url=url,
        )

    @staticmethod
    def empty(name: str = "URL") -> "Url":
        return Url(name=name)

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
