from abc import ABC
from typing import Type, ClassVar


class ABCEvent(ABC):
    bases: ClassVar

    def __init_subclass__(cls: Type["ABCEvent"]):
        bases = frozenset(base for base in cls.mro() if issubclass(base, ABCEvent.__subclasses__()[0]))
        cls.bases = staticmethod(lambda: bases)


# TODO:
class Event(ABCEvent):
    @staticmethod
    def bases() -> frozenset[Type["Event"]]:
        return frozenset([Event])
