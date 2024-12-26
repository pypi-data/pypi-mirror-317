from dataclasses import dataclass

from .property import Property


@dataclass
class Button(Property):
    id: str
    name: str
    type: str = "button"

    @staticmethod
    def of(key: str, property: dict) -> "Button":
        return Button(id=property["id"], name=key)

    def value_for_filter(self) -> str:
        raise NotImplementedError

    def __dict__(self) -> dict:
        return {
            self.name: {
                "id": self.id,
                "type": self.type,
                "button": {},
            },
        }
