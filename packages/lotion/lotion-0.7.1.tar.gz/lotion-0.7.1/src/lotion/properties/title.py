from dataclasses import dataclass
from typing import Any, Type, TypeVar

from lotion.block.rich_text.rich_text import RichText
from lotion.block.rich_text.rich_text_builder import RichTextBuilder

from .property import Property

T = TypeVar("T", bound="Title")


@dataclass
class Title(Property):
    # text: str
    # value: list[dict]
    rich_text: RichText
    type: str = "title"
    # mentioned_page_id: str | None = None

    def __init__(
        self,
        name: str,
        rich_text: RichText,
        id: str | None = None,
    ):
        self.name = name
        self.id = id
        self.rich_text = rich_text

    @classmethod
    def from_properties(cls: Type[T], properties: dict) -> T:
        if "Name" in properties:
            return cls.__of("Name", properties["Name"])
        if "Title" in properties:
            return cls.__of("Title", properties["Title"])
        if "名前" in properties:
            return cls.__of("名前", properties["名前"])
        msg = f"Title property not found. properties: {properties}"
        raise Exception(msg)

    @classmethod
    def from_property(cls: Type[T], key: str, property: dict) -> T:
        return cls.__of(key, property)

    def __dict__(self) -> dict:
        result: dict[str, Any] = {
            "title": self.rich_text.to_dict(),
        }
        if self.id is not None:
            result["id"] = self.id
        return {
            self.name: result,
        }

    @classmethod
    def __of(cls: Type[T], name: str, param: dict) -> T:
        rich_text = RichText.from_entity(param["title"])
        return cls(
            name=name,
            id=param["id"],
            rich_text=rich_text,
        )

    @classmethod
    def from_plain_text(cls: Type[T], name: str = "名前", text: str = "") -> T:
        rich_text = RichText.from_plain_text(text)
        return cls(
            name=name,
            rich_text=rich_text,
        )

    @classmethod
    def from_rich_text(cls: Type[T], name: str, rich_text: RichText) -> T:
        return cls(
            name=name,
            rich_text=rich_text,
        )

    @classmethod
    def from_mentioned_page(
        cls: Type[T],
        mentioned_page_id: str,
        name: str = "名前",
        prefix: str = "",
        suffix: str = "",
    ) -> T:
        rich_text_builder = RichTextBuilder.create()
        if prefix != "":
            rich_text_builder.add_text(prefix)
        rich_text_builder.add_page_mention(mentioned_page_id)
        if suffix != "":
            rich_text_builder.add_text(suffix)
        return cls(
            name=name,
            rich_text=rich_text_builder.build(),
        )

    @staticmethod
    def from_mentioned_page_id(
        page_id: str,
        name: str = "名前",
    ) -> "Title":
        rich_text_builder = RichTextBuilder.create()
        rich_text_builder.add_page_mention(page_id)
        return Title(
            name=name,
            rich_text=rich_text_builder.build(),
        )

    @property
    def text(self) -> str:
        return self.rich_text.to_plain_text()

    def value_for_filter(self) -> str:
        return self.text
