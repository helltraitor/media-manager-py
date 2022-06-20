from media_manager.application.api.context import Context
from media_manager.application.api.messages import MessageClient

from .abc import Component


class CMessageClient(Component):
    def __init__(self, context: Context):
        super().__init__(context)
        self.__client = context.unwrap(MessageClient.__name__, MessageClient)

    def client(self) -> MessageClient:
        return self.__client
