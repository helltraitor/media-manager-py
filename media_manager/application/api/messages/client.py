import logging

from abc import ABC

from typing import Generator, Protocol

from media_manager.application import utils

from .credits import Credits
from .handler import MessageHandler
from .message import SignableMessage
from .result import Result
from .target import Target


class MessageServer(Protocol):
    def login(self, client: "MessageClient"): ...

    def logout(self, client: "MessageClient"): ...

    def send(self, client: "MessageClient", target: Target, message: SignableMessage) -> Result: ...


class MessageClient(ABC):
    def __init__(self, credits: Credits):
        self.__credits = credits
        self.__handlers: dict[str, MessageHandler] = {}
        self.__server: MessageServer | None = None

    def __del__(self):
        self.disconnect()

    def add_handler(self, key: str, handler: MessageHandler):
        self.__handlers[key] = handler

    def credits(self) -> Credits:
        return self.__credits.copy()

    def connected(self) -> bool:
        return self.__server is not None

    def connect(self, server: MessageServer):
        if self.__server is not None:
            if self.__server is server:
                logging.error('%s: Attempting to connect client to the same server twice',
                              utils.name(self))
                return
            logging.warning('%s: Client is reconnected. Reconnection may cause further errors',
                            utils.name(self))
            self.disconnect()
        self.__server = server
        self.__server.login(self)

    def delete_handler(self, key: str):
        if key not in self.__handlers:
            logging.warning("%s: Attempting to delete non-existing handler with key %s",
                            utils.name(self), key)
            return
        del self.__handlers[key]

    def disconnect(self):
        if self.__server is None:
            logging.error('%s: Attempting to close server while no connection exists',
                          utils.name(self))
            raise RuntimeError("Unable to disconnect. Client is not logon")
        self.__server.logout(self)

    def handlers(self, credits: Credits) -> Generator[MessageHandler, None, None]:
        for handler in self.__handlers.values():
            if handler.accepts(credits):
                yield handler

    def send(self, target: Target, message: SignableMessage) -> Result:
        if self.__server is None:
            logging.error("%s: Attempting to send message when client is not logon on any server",
                          utils.name(self))
            raise RuntimeError("Client was not connect to the server")
        return self.__server.send(self, target, message)
