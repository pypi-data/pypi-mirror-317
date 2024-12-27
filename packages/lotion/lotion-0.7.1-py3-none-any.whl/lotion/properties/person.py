from dataclasses import dataclass
from typing import Type, TypeVar

from .property import Property

T = TypeVar("T", bound="People")


@dataclass
class People(Property):
    """
        ユーザプロパティ

        ex.{'id': '%5Eo%5Dy', 'type': 'people', 'people': [{'object': 'user', 'id': '
    6f877603-07b9-4467-b811-31706eeb640c', 'name': 'Akira Kobori', 'avatar_url': 'https://s3-us-west-2.amazonaws.com/public.notion-static.c
    om/1f3a184f-88f3-4048-bb77-3bef8ff805d8/kobori_akira_blackline.png', 'type': 'person', 'person': {'email': 'private.beats@gmail.com'}}]
    }
    """

    def __init__(self, name: str, id: str | None = None, people_list: list | None = None) -> None:  # noqa: A002, FBT001
        self.name = name
        self.id = id
        self.people_list = people_list

    @classmethod
    def of(cls: Type[T], name: str, param: dict) -> T:
        id = param["id"]
        people_list = param["people"]
        return cls(
            name=name,
            id=id,
            people_list=people_list,
        )

    @property
    def type(self) -> str:
        return "people"

    def __dict__(self) -> dict:
        result = {
            "type": self.type,
            self.type: self.people_list,
        }
        if self.id is not None:
            result["id"] = self.id
        return {self.name: result}

    def value_for_filter(self) -> str:
        raise NotImplementedError
