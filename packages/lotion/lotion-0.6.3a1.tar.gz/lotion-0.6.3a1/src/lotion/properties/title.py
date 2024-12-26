from dataclasses import dataclass

from ..block.rich_text.rich_text_element import (
    RichTextMentionElement,
    RichTextTextElement,
)
from ..page.page_id import PageId
from .property import Property


@dataclass
class Title(Property):
    text: str
    value: list[dict]
    type: str = "title"
    mentioned_page_id: str | None = None

    def __init__(
        self,
        name: str,
        id: str | None = None,
        value: list[dict] = [],
        text: str | None = None,
        mentioned_page_id: str | None = None,
    ):
        self.name = name
        self.id = id
        self.value = value
        self.text = text
        self.mentioned_page_id = mentioned_page_id

    @classmethod
    def from_properties(cls, properties: dict) -> "Title":
        if "Name" in properties:
            return cls.__of("Name", properties["Name"])
        if "Title" in properties:
            return cls.__of("Title", properties["Title"])
        if "名前" in properties:
            return cls.__of("名前", properties["名前"])
        msg = f"Title property not found. properties: {properties}"
        raise Exception(msg)

    @classmethod
    def from_property(cls, key: str, property: dict) -> "Title":
        return cls.__of(key, property)

    def __dict__(self) -> dict:
        result = {
            "title": self._get_value(),
        }
        if self.id is not None:
            result["id"] = self.id
        return {
            self.name: result,
        }

    def _get_value(self) -> list[dict]:
        if self.value is not None and self.value != []:
            return self.value
        values = []
        values.append(
            {
                "type": "text",
                "text": {
                    "content": self.text,
                },
            },
        )
        if self.mentioned_page_id is not None:
            values.append(
                {
                    "type": "mention",
                    "mention": {
                        "type": "page",
                        "page": {
                            "id": self.mentioned_page_id,
                        },
                    },
                    # "plain_text": self.text,
                    # "href": f"https://www.notion.so/{self.mentioned_page_id}"
                },
            )
        return values

    @staticmethod
    def __of(name: str, param: dict) -> "Title":
        return Title(
            name=name,
            id=param["id"],
            value=param["title"],
            text="".join([item["plain_text"] for item in param["title"]]),
        )

    @staticmethod
    def from_plain_text(name: str = "名前", text: str = "") -> "Title":
        return Title(
            name=name,
            text=text,
        )

    @staticmethod
    def from_mentioned_page(
        mentioned_page_id: str,
        mentioned_page_title: str,
        name: str = "名前",
        prefix: str = "",
        suffix: str = "",
    ) -> "Title":
        title = prefix + mentioned_page_title + suffix
        values = []
        if prefix != "":
            rich_text_element = RichTextTextElement.of(content=prefix)
            values.append(rich_text_element.to_dict())
        page_id_object = PageId(mentioned_page_id)
        rich_text_element = RichTextMentionElement.from_page_type(page_id_object.value)
        values.append(rich_text_element.to_dict())
        if suffix != "":
            rich_text_element = RichTextTextElement.of(content=suffix)
            values.append(rich_text_element.to_dict())
        return Title(
            name=name,
            value=values,
            text=title,
        )

    @staticmethod
    def from_mentioned_page_id(
        page_id: str,
        name: str = "名前",
    ) -> "Title":
        return Title(
            name=name,
            text="",
            mentioned_page_id=page_id,
        )

    def value_for_filter(self) -> str:
        return self.text
