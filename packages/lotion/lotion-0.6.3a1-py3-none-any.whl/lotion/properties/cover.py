from dataclasses import dataclass
from typing import Any


@dataclass
class Cover:
    type: str
    external_url: str | None = None

    def __init__(
        self, type: str, external_url: str | None = None
    ) -> None:  # noqa: A002
        self.type = type
        self.external_url = external_url

    @staticmethod
    def of(param: dict) -> "Cover":
        return Cover(
            type=param["type"],
            external_url=param["external"]["url"] if "external" in param else None,
        )

    @staticmethod
    def from_external_url(external_url: str) -> "Cover":
        return Cover(
            type="external",
            external_url=external_url,
        )

    def __dict__(self) -> dict:
        result: dict[str, Any] = {
            "type": self.type,
        }
        if self.external_url is not None:
            result["external"] = {
                "url": self.external_url,
            }
        return result

    def value_for_filter(self) -> str:
        raise NotImplementedError
