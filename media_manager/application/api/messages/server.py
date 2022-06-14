import logging

from queue import Queue

from .client import MessageClient
from .message import Message


class MessageServer:
    def __init__(self):
        self.__clients: dict[str, MessageClient] = {}
        self.__messages: Queue[tuple[MessageClient, Message]] = Queue()

    def login(self, client: MessageClient):
        if client.id() in self.__clients:
            logging.error(f'{type(self).__name__}: Attempting to login with same id: {client.id()}')
            return
        self.__clients[client.id()] = client

    def logout(self, client: MessageClient):
        if client.id() not in self.__clients:
            logging.error(f'{type(self).__name__}: Attempting to login with same id: {client.id()}')
            return
        del self.__clients[client.id()]

    def send(self, client: MessageClient, target: dict[str, str], message: Message) -> bool | None:
        if client.id() not in self.__clients:
            return False

        sent: bool | None = None
        for other in self.__clients.values():
            if self.same_credits(target, other.credits()) and other.accepts(client.credits()):
                self.__messages.put((other, message))
                sent = True
        return sent

    @staticmethod
    def same_credits(lhs: dict[str, str], rhs: dict[str, str]) -> bool:
        topics = set(lhs.keys()).intersection(set(rhs.keys()))
        return all(lhs[topic] == rhs[topic] for topic in topics)

    def process(self):
        if not self.__messages.empty():
            client, message = self.__messages.get()
            if client.id() in self.__clients:
                reply = client.receive(message)
                message.handle(reply)
