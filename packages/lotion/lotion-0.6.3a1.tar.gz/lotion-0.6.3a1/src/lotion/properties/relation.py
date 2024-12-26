from dataclasses import dataclass

from .property import Property


@dataclass
class Relation(Property):
    id_list: list[str]
    text_list: list[str]  # NOTE: Notionのデータとしては扱わない。id_listに変換するために必要になることが多いため
    type: str = "relation"
    has_more: bool = False

    TYPE = "relation"

    def __init__(  # noqa: PLR0913
        self,
        name: str,
        id: str | None = None,  # noqa: A002
        id_list: list[str] | None = None,
        text_list: list[str] | None = None,
        has_more: bool | None = None,
    ) -> None:
        self.name = name
        self.id = id
        self.id_list = id_list or []
        self.text_list = text_list or []
        self.has_more = bool(has_more)

    def is_unconverted_id_list(self) -> bool:
        """text_listがあるがid_listがない場合にTrueを返す"""
        return len(self.text_list) > 0 and len(self.id_list) == 0

    @staticmethod
    def of(name: str, property: dict[str, str]) -> "Relation":  # noqa: A002
        id_list = [r["id"] for r in property["relation"]]
        return Relation(name=name, id_list=id_list, has_more=property["has_more"])

    @staticmethod
    def from_id_list(name: str, id_list: list[str]) -> "Relation":
        return Relation(
            name=name,
            id_list=id_list,
        )

    @staticmethod
    def from_id(name: str, id: str) -> "Relation":
        return Relation.from_id_list(name=name, id_list=[id])

    def __dict__(self) -> dict:
        result = {
            "type": self.type,
            "relation": [
                {
                    "id": id,
                }
                for id in self.id_list  # noqa: A001
            ],
            "has_more": self.has_more,
        }
        if self.id is not None:
            result["relation"]["id"] = self.id
        return {
            self.name: result,
        }

    def value_for_filter(self) -> str:
        raise NotImplementedError
