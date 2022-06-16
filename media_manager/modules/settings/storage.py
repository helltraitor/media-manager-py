from typing import Callable


class Storage:
    ONLINE_STORAGE: dict[str, str] = {}
    CALLBACKS: dict[str, list[Callable[[], None]]] = {}

    def __init__(self):
        self.__online = self.ONLINE_STORAGE
        self.__callbacks = self.CALLBACKS

    def all(self) -> dict[str, str]:
        self.notify("all")
        return self.__online.copy()

    def get(self, key: str, default: str | None = None) -> str | None:
        self.notify("get")
        return self.__online.get(key, default)

    def set(self, key: str, value: str):
        self.__online[key] = value
        self.notify("set")

    def delete(self, key: str) -> bool:
        if key in self.__online:
            del self.__online[key]
            self.notify("delete")
            return True
        return False


    def notify(self, action: str):
        for callback in self.__callbacks.get(action, ()):
            callback()

    def subscribe(self, action: str, callback: Callable[[], None]):
        if action not in self.__callbacks:
            self.__callbacks[action] = []
        self.__callbacks[action].append(callback)
