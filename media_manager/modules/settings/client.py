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

from .storage import Storage, Lifetime


class CSettingsMessageClient(CMessageClient):
    def __init__(self, context: Context):
        super().__init__(context)
        self.__storage = context.unwrap("storage", Storage)
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

        domain = self.__storage.ensure_get(message.credits().name())
        match message.content().get("action", None):
            case "delete":
                if (key := message.content().get("key", None)) is None:
                    return Reply(Result("ERROR", "Key in action was not set"))
                logging.debug("Deleted key %s", key)
                domain.delete(key)

            case "get":
                if (key := message.content().get("key", None)) is None:
                    return Reply(Result("ERROR", "Key in action was not set"))
                if (record := domain.get(key, message.content().get("default", None))) is None:
                    logging.debug("NO KEY %s", key)
                    return Reply(Result("ERROR", f"No value for key {key}"))
                logging.debug("Got key %s with value %s", key, record.value)
                return Reply(Result("OK"), content={"value": record.value.decode()})

            case "set":
                if (key := message.content().get("key", None)) is None:
                    return Reply(Result("ERROR", "Key in action was not set"))
                if (value := message.content().get("value", None)) is None:
                    return Reply(Result("ERROR", f"No value for key {key}"))

                seconds = message.content().get("lifetime_seconds", None)
                lifetime = Lifetime.default() if seconds is None else Lifetime(seconds=int(seconds))

                logging.debug("Set key %s with value %s and lifetime seconds %s", key, value, lifetime.seconds_left())
                domain.set(key, value.encode(), lifetime)

            case "pop":
                if (key := message.content().get("key", None)) is None:
                    return Reply(Result("ERROR", "Key in action was not set"))
                default = message.content().get("value", None)

                record = domain.pop(key, default and default.encode())
                if record is not None:
                    logging.debug("Popped key %s with value %s", key, record.value)
                    return Reply(Result("OK"), content={"value": record.value.decode()})

            case "replace":
                if (key := message.content().get("key", None)) is None:
                    return Reply(Result("ERROR", "Key in action was not set"))
                if (value := message.content().get("value", None)) is None:
                    return Reply(Result("ERROR", f"No value for key {key}"))

                seconds = message.content().get("lifetime_seconds", None)
                lifetime = Lifetime.default() if seconds is None else Lifetime(seconds=int(seconds))

                record = domain.replace(key, value.encode(), lifetime)
                if record is not None:
                    logging.debug("Replaced key %s with value %s", key, record.value)
                    return Reply(Result("OK"), content={"value": record.value.decode()})

            case None:
                return Reply(Result("ERROR", "Action was not set"))

            case other:
                return Reply(Result("ERROR", f"Unknown action: {other}"))
        return Reply(Result("OK"))
