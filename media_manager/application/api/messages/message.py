from abc import ABC
from typing import Callable

from .reply import Reply


class Message(ABC):
    def __init__(self, content: dict[str, str]):
        self.__content = content
        self.__handled = False

    def content(self) -> dict[str, str]:
        return self.__content

    def handled(self) -> bool:
        return self.__handled

    def handle(self, reply: Reply):
        if not self.__handled:
            self.__handled = True
            self.process(reply)

    def process(self, reply: Reply):
        pass


class CallbackMessage(Message):
    def __init__(self, handler: Callable[[Reply], None], content: dict[str, str]):
        super().__init__(content)
        self.__handler = handler

    def process(self, reply: Reply):
        self.__handler(reply)
