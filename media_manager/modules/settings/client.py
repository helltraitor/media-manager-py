import logging

from media_manager.application.api.messages import MessageClient, Message, Reply

from .storage import Storage


class ProtectedModuleClient(MessageClient):
    def __init__(self):
        super().__init__("Settings 0.0.1", {"name": "Settings"})
        self.__storage = Storage()

    def accepts(self, credits: dict[str, str]) -> bool:
        return True

    def receive(self, message: Message) -> Reply:
        logging.info(message.content())

        action = message.content().get("action", None)
        if action is None:
            return Reply({"status": "ERROR", "reason": "Action was not set"})
        elif action not in ("get", "set", "delete", "update"):
            return Reply({"status": "ERROR", "reason": f"Unknown action `{action}`"})

        if action == "get":
            key = message.content().get("key", None)
            if key is None:
                return Reply({"status": "ERROR", "reason": "Key was not set"})
            value = self.__storage.get(key)
            if value is None:
                return Reply({"status": "ERROR", "reason": "No value under such key"})
            return Reply({"status": "OK", "value": value})

        if action == "set":
            key = message.content().get("key", None)
            if key is None:
                return Reply({"status": "ERROR", "reason": "Key was not set"})
            value = message.content().get("value", None)
            if value is None:
                return Reply({"status": "ERROR", "reason": "Value was not set"})
            self.__storage.set(key, value)
            return Reply({"status": "OK"})

        if action == "delete":
            key = message.content().get("key", None)
            if key is None:
                return Reply({"status": "ERROR", "reason": "Key was not set"})
            if not self.__storage.delete(key):
                return Reply({"status": "ERROR", "reason": "No such key"})
            return Reply({"status": "OK"})
        return Reply({"status": "ERROR", "reason": "Unexpected error"})
