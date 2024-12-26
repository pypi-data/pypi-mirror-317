from dataclasses import dataclass

from .property import Property


@dataclass
class Status(Property):
    status_id: str | None
    status_name: str
    status_color: str | None
    type: str = "status"

    def __init__(
        self,
        name: str,
        status_name: str,
        id: str | None = None,
        status_id: str | None = None,
        status_color: str | None = None,
    ):
        self.name = name
        self.status_name = status_name
        self.id = id
        self.status_id = status_id
        self.status_color = status_color

    @staticmethod
    def of(name: str, param: dict) -> "Status":
        return Status(
            name=name,
            status_name=param["status"]["name"],
            id=param["id"],
            status_id=param["status"]["id"],
            status_color=param["status"]["color"],
        )

    @staticmethod
    def from_status_name(name: str, status_name: str) -> "Status":
        return Status(
            name=name,
            status_name=status_name,
        )

    def is_today(self) -> bool:
        return self.status_name == "Today"

    def __dict__(self):
        result = {
            "type": self.type,
            "status": {
                "name": self.status_name,
            },
        }
        if self.status_id is not None:
            result["status"]["id"] = self.status_id
        if self.status_color is not None:
            result["status"]["color"] = self.status_color
        return {self.name: result}

    def value_for_filter(self) -> str:
        return self.status_name
