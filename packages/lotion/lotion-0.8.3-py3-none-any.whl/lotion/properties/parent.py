from dataclasses import dataclass


@dataclass
class Parent:
    type: str
    workspace: bool | None = None

    def value_for_filter(self) -> str:
        raise NotImplementedError
