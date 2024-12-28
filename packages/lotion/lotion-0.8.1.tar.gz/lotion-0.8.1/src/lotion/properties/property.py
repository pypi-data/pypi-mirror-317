from abc import ABCMeta, abstractmethod


class Property(metaclass=ABCMeta):
    id: str | None
    name: str
    type: str
    PROP_NAME: str = "Property"  # Must be overridden

    @abstractmethod
    def __dict__(self) -> dict:
        pass

    @abstractmethod
    def value_for_filter(self):  # noqa: ANN201
        pass
