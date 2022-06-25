import logging

from queue import Queue
from typing import NamedTuple

from media_manager.application import utils

from .client import MessageClient
from .handler import MessageHandler
from .message import SignedMessage, SignableMessage
from .result import Result
from .target import Target


class QueuedMessage(NamedTuple):
    handler: MessageHandler
    message: SignedMessage

    def process(self):
        # Here locates some disturbing repeated but different methods.
        # These methods must be named same, but they have different context
        #
        # Handler processes a sent message and receives the reply
        reply = self.handler.process(self.message)
        # Then message process method or special callback processes the reply
        self.message.process(reply)


class MessageServer:
    def __init__(self):
        self.__clients: dict[str, MessageClient] = {}
        self.__messages: Queue[QueuedMessage] = Queue()

    def login(self, client: MessageClient):
        client_id = client.credits().id()
        if client_id in self.__clients:
            logging.error('%s: Attempting to login with same id: %s',
                          utils.name(self), client_id)
            return
        self.__clients[client_id] = client

    def logout(self, client: MessageClient):
        client_id = client.credits().id()
        if client_id not in self.__clients:
            logging.error('%s: Attempting to logout with same id: %s',
                          utils.name(self), client_id)
            return
        del self.__clients[client_id]

    def send(self, client: MessageClient, target: Target, message: SignableMessage) -> Result:
        if client.credits().id() not in self.__clients:
            return Result("ERROR", "Client was not logon on this server")

        for other in self.__clients.values():
            if not target.match(other.credits()):
                continue
            for handler in other.handlers(client.credits()):
                self.__messages.put(QueuedMessage(handler, message.sign(client.credits())))
        return Result("OK")

    def process(self):
        if not self.__messages.empty():
            self.__messages.get().process()
