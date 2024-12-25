from abc import ABC, abstractmethod
from typing import Dict, Any


class Object(ABC):
    def __init__(self, **kwargs) -> None:
        slot: str
        for slot in self.__slots__:
            if slot in kwargs:
                setattr(self, slot, kwargs.pop(slot))

            else:
                setattr(self, slot, None)

        for kwarg in kwargs:
            raise KeyError(
                "Object '" + str(self.__class__) + "' has no key '" + kwarg + "'"
            )

    @staticmethod
    @abstractmethod
    def from_dict(raw_data: Dict[str, Any]) -> "Object":
        raise Exception()

    def __repr__(self) -> str:
        output: str = "cforces.types<" + self.__class__.__name__ + ">"
        data: Dict[str, Any] = {}

        slot: str
        for slot in self.__slots__:
            if hasattr(self, slot):
                data[slot] = getattr(self, slot)

            else:
                data[slot] = None

        return output + str(data)
