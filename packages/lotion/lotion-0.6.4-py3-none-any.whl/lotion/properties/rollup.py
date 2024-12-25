from dataclasses import dataclass

from .property import Property


@dataclass
class Rollup(Property):
    """Rollup class

    ex.
    {'id': '%3BXyX', 'type': 'rollup', 'rollup': {'type': 'number', 'number': 0, 'function': 'count_values'}}
    """

    _rollup: dict

    def __init__(
        self,
        name: str,
        rollup: dict = {},
        id: str | None = None,  # noqa: A002
    ) -> None:
        self.name = name
        self._rollup = rollup
        self.id = id

    @staticmethod
    def of(key: str, param: dict) -> "Rollup":
        return Rollup(
            id=param["id"],
            name=key,
            rollup=param["rollup"],
        )

    @property
    def value(self) -> dict:
        rollup_type = self._rollup["type"]
        return self._rollup[rollup_type]

    @property
    def type(self) -> str:
        return "rollup"

    def __dict__(self) -> dict:
        raise NotImplementedError("this dict method must not be called")

    def value_for_filter(self) -> str:
        raise NotImplementedError
