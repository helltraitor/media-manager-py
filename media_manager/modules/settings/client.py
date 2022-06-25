import logging

from media_manager.application.api.context import Context
from media_manager.application.api.messages import (
    Credits,
    MessageHandler,
    Reply,
    Result,
    SignedMessage
)
from media_manager.application.api.module.components import CMessageClient
from media_manager.application.api.module.features import FMessages

from .storage import Storage


class CSettingsMessageClient(CMessageClient):
    def __init__(self, context: Context):
        super().__init__(context)
        self.__storage = Storage()
        self.__setup()

    def __setup(self):
        self.client().add_handler("any", SettingsMessageAnyHandler(self.__storage))


class SettingsMessageAnyHandler(MessageHandler):
    def __init__(self, storage: Storage):
        self.__storage = storage

    def accepts(self, _: Credits) -> bool:
        return True

    def process(self, message: SignedMessage) -> Reply:
        logging.debug("%s: Received message from %s with content: %s",
                      type(self).__name__, message.credits(), message.content())

        domain = self.__storage.domain(message.credits().id())
        match message.content().get("action", None):
            case "delete":
                if (key := message.content().get("key", None)) is None:
                    return Reply(Result("ERROR", "Key in action was not set"))

                default = message.content().get("returning", None)
                if default is not None:
                    returning = domain.delete(key, default)
                    return Reply(Result("OK"), content={"value": str(returning)})
                if domain.delete(key) is not None:
                    return Reply(Result("OK"))
                return Reply(Result("ERROR", f"Key {key} not in storage"))

            case "get":
                if (key := message.content().get("key", None)) is None:
                    return Reply(Result("ERROR", "Key in action was not set"))
                if (value := domain.get(key, message.content().get("default", None))) is None:
                    return Reply(Result("ERROR", f"No value for key {key}"))
                return Reply(Result("OK"), content={"value": value})

            case "set":
                if (key := message.content().get("key", None)) is None:
                    return Reply(Result("ERROR", "Key in action was not set"))
                if (value := message.content().get("value", None)) is None:
                    return Reply(Result("ERROR", f"No value for key {key}"))
                domain.set(key, value)
                return Reply(Result("OK"))

            case "update":
                if (key := message.content().get("key", None)) is None:
                    return Reply(Result("ERROR", "Key in action was not set"))
                if (value := message.content().get("value", None)) is None:
                    return Reply(Result("ERROR", f"No value for key {key}"))
                if (returning := message.content().get("returning", None)) is None:
                    return Reply(Result("ERROR", "Returning value is not specified"))
                return Reply(Result("OK"), content={"value": domain.update(key, value, returning)})

            case None:
                return Reply(Result("ERROR", "Action was not set"))

            case other:
                return Reply(Result("ERROR", f"Unknown action: {other}"))
