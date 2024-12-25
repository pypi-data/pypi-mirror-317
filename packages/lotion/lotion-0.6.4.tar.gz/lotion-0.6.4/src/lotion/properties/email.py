from dataclasses import dataclass

from .property import Property


@dataclass
class Email(Property):
    """Email class

    ex.
    {'id': 'Io%7C%3A', 'type': 'email', 'email': 'sample@example.com'}
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
    def of(key: str, param: dict) -> "Email":
        value = param.get("email")
        if value is not None and not isinstance(value, str):
            raise ValueError(f"email must be str, but got {type(value)}")
        return Email(id=param["id"], name=key, value=value or "")

    @staticmethod
    def from_email(name: str, email: str) -> "Email":
        return Email(name=name, value=email)

    @staticmethod
    def empty(name: str) -> "Email":
        return Email(name=name)

    @property
    def type(self) -> str:
        return "email"

    def __dict__(self) -> dict:
        result = {
            "type": self.type,
            "email": None if self.value == "" else self.value,
        }
        if self.id is not None:
            result["id"] = self.id
        return {
            self.name: result,
        }

    def value_for_filter(self) -> str:
        raise NotImplementedError
