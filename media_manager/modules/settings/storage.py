from typing import Callable


class DomainStorage:
    def __init__(self, domain: dict[str, str]):
        self.__domain = domain
        self.__callbacks: dict[str, list[Callable[[], None]]] = {}

    def all(self) -> dict[str, str]:
        items = self.__domain.copy()
        self.notify("all")
        return items

    def get(self, key: str, default: str | None = None) -> str | None:
        value = self.__domain.get(key, default)
        self.notify("get")
        return value

    def set(self, key: str, value: str):
        self.__domain[key] = value
        self.notify("set")

    def delete(self, key: str, default: str | None = None) -> str | None:
        returning = self.__domain.pop(key, default)
        self.notify("delete")
        return returning

    def update(self, key: str, value: str, default: str) -> str:
        returning = self.__domain.get(key, default)
        self.__domain[key] = value
        self.notify("update")
        return returning

    def notify(self, action: str):
        for callback in self.__callbacks.get(action, ()):
            callback()

    def subscribe(self, action: str, callback: Callable[[], None]):
        if action not in self.__callbacks:
            self.__callbacks[action] = []
        self.__callbacks[action].append(callback)


class Storage:
    ONLINE_DOMAINS: dict[str, DomainStorage] = {}
    ONLINE_STORAGE: dict[str, dict[str, str]] = {}
    GLOBAL_CALLBACKS: dict[str, list[Callable[[], None]]] = {}

    def __init__(self):
        self.__callbacks = self.GLOBAL_CALLBACKS
        self.__domains = self.ONLINE_DOMAINS
        self.__online = self.ONLINE_STORAGE

    def exists(self, id: str) -> bool:
        return id in self.__online

    def domain(self, id: str) -> DomainStorage:
        if id in self.__domains:
            return self.__domains[id]

        if id in self.__online:
            self.__domains[id] = DomainStorage(self.__online[id])
            return self.__domains[id]

        self.__online[id] = {}
        self.__domains[id] = DomainStorage(self.__online[id])
        self.subscribe_globals(domain=self.__domains[id])
        return self.__domains[id]

    def subscribe(self, *, action: str, callback: Callable[[], None]):
        if action not in self.__callbacks:
            self.__callbacks[action] = []

        self.GLOBAL_CALLBACKS[action].append(callback)
        for domain in self.__domains.values():
            domain.subscribe(action, callback)

    def subscribe_globals(self, *, domain: DomainStorage):
        for action, callbacks in self.__callbacks.items():
            for callback in callbacks:
                domain.subscribe(action, callback)
