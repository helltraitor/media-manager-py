from abc import ABC, abstractmethod
from time import time
from typing import Callable, Any


class Deferred(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def expected(self) -> int:
        pass

    @abstractmethod
    def pending(self) -> bool:
        pass


class DeferredCall(Deferred):
    def __init__(self, callable: Callable[[], Any], *, milliseconds: int | None = None):
        self.__callable = callable
        self.__expected = int(time() * 1000) + (milliseconds or 0)

    def execute(self):
        self.__callable()

    def expected(self) -> int:
        return self.__expected

    def pending(self) -> bool:
        return self.__expected < time() * 1000
