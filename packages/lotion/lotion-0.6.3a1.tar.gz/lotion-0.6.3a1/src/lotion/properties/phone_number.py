from dataclasses import dataclass

from .property import Property


@dataclass
class PhoneNumber(Property):
    """PhoneNumber class

    ex.
    {'id': 'FCsG', 'type': 'phone_number', 'phone_number': '03-1234-5678'}
    """

    value: str

    def __init__(
        self,
        name: str,
        value: str = "",
        id: str | None = None,  # noqa: A002
    ) -> None:
        self.name = name
        self.value = value
        self.id = id

    @staticmethod
    def of(key: str, param: dict) -> "PhoneNumber":
        value = param.get("phone_number")
        if value is not None and not isinstance(value, str):
            raise ValueError(f"phone_number must be str, but got {type(value)}")
        return PhoneNumber(id=param["id"], name=key, value=value or "")

    @staticmethod
    def empty(name: str) -> "PhoneNumber":
        return PhoneNumber(name=name)

    @staticmethod
    def create(name: str, phone_number: str) -> "PhoneNumber":
        return PhoneNumber(name=name, value=phone_number)

    @property
    def type(self) -> str:
        return "phone_number"

    def __dict__(self) -> dict:
        result = {
            "type": self.type,
            "phone_number": self.value if self.value != "" else None,
        }
        if self.id is not None:
            result["id"] = self.id
        return {
            self.name: result,
        }

    def value_for_filter(self) -> str:
        raise NotImplementedError
