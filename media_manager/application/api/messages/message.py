from abc import ABC
from typing import Any, Callable, TypeAlias

from .reply import Reply
from .credits import Credits


Content: TypeAlias = dict[str, str]


class Message(ABC):
    def __init__(self, content: Content):
        self.__content = content
        self.__handled = False

    def content(self) -> Content:
        return self.__content

    def handled(self) -> bool:
        return self.__handled

    def handle(self, reply: Reply):
        if not self.handled():
            self.__handled = True
            self.process(reply)

    def process(self, reply: Reply):
        pass


class SignedMessage(Message):
    def __init__(self, credits: Credits, content: Content, handler: Callable[[Reply], Any]):
        super().__init__(content)
        self.__credits = credits
        self.__handler = handler

    def credits(self) -> Credits:
        return self.__credits

    def process(self, reply: Reply):
        self.__handler(reply)


class SignableMessage(Message):
    def sign(self, credits: Credits) -> SignedMessage:
        return SignedMessage(credits, self.content(), self.process)


class CallbackMessage(SignableMessage):
    def __init__(self, content: Content, handler: Callable[[Reply], Any]):
        super().__init__(content)
        self.__handler = handler

    def process(self, reply: Reply):
        self.__handler(reply)
