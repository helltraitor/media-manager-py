import logging

from abc import ABC

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .server import MessageServer

from .message import Message
from .reply import Reply


class MessageClient(ABC):
    def __init__(self, id: str, credits: dict[str, str]):
        self.__id = id
        self.__credits = credits
        self.__server: "MessageServer | None" = None

    def accepts(self, credits: dict[str, str]) -> bool:
        return False

    def credits(self) -> dict[str, str]:
        return self.__credits.copy()

    def connected(self) -> bool:
        return self.__server is not None

    def connect(self, server: "MessageServer"):
        if self.__server is not None:
            if self.__server is server:
                logging.error(f'{type(self).__name__}: Attempting to connect client to its server again')
                return
            logging.warning(f'{type(self).__name__}: Reconnection may cause further errors')
            self.disconnect()
        self.__server = server
        self.__server.login(self)

    def disconnect(self):
        if self.__server is None:
            logging.error(f'{type(self).__name__}: Attempting to close server while no connection exists')
            raise RuntimeError
        MessageServer.logout(self.__server, self)
        self.__server.logout(self)

    def id(self) -> str:
        return self.__id

    def send(self, target: dict[str, str], message: Message) -> bool | None:
        # None - not found
        # True - Received
        # False - Error
        return self.__server.send(self, target, message)

    def receive(self, message: Message) -> Reply:
        return Reply({})
