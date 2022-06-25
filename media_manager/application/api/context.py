import logging

from typing import Any, NamedTuple, Type, TypeVar

from media_manager.application.api.deferred import DeferredPool, DeferredPoolChannel
from media_manager.application.api.messages import MessageServer, MessageClient
from media_manager.application import utils


T = TypeVar("T")


class ContextItem(NamedTuple):
    visible: bool
    value: Any


class Context:
    def __init__(self, **items: ContextItem):
        self.__storage: dict[str, ContextItem] = items

    def __get(self, name: str, *, respectful: bool = True) -> ContextItem | None:
        if name not in self.__storage:
            return None

        item = self.__storage[name]
        if not respectful or item.visible:
            return item
        return None

    def __get_casted(self, name: str, guard: Type[T], *, critical: bool = True, respectful: bool = True) -> T | None:
        item = self.__get(name, respectful=respectful)
        if item is None:
            if not critical:
                return None
            logging.warning("%s: Attempting to get `%s` with type %s. `%s` is out of context",
                            utils.name(self), name, utils.name(guard), utils.name(guard))
            raise RuntimeError(f"Name `{name}` out of context")

        if not isinstance(item.value, guard):
            if not critical:
                return None
            logging.warning("%s: Attempting to get `%s` with type %s. `%s` is not instance of %s",
                            utils.name(self), name, utils.name(guard), name, utils.name(guard))
            raise RuntimeError(f"{type(item.value)} is not isinstance of guard type {guard}")
        return item.value

    def auto(self, name: str, *, critical: bool = True) -> Any | None:
        match name:
            case DeferredPoolChannel.__name__:
                pool = self.__get_casted(DeferredPool.__name__, DeferredPool, critical=critical, respectful=False)
                if pool is not None:
                    return pool.channel()
                return None

            case MessageClient.__name__:
                server = self.__get_casted(MessageServer.__name__, MessageServer, critical=critical, respectful=False)
                if server is None:
                    return None

                client_id = self.checked("id", str, critical=False)
                client_credits = self.checked("credits", dict, critical=False)
                if not client_id or not client_credits:
                    logging.error("%s: Attempting to create client with wrong id and credits: %s and %s",
                                  utils.name(self), utils.name(client_id), utils.name(client_credits))
                    raise RuntimeError(
                        f"{utils.name(MessageClient)} requires both `id` and `credits` with types `str` and `dict`")

                client = MessageClient(client_id, client_credits)
                client.connect(server)
                return client

        return self.manual(name, critical=critical)

    def checked(self, name: str, guard: Type[T]) -> T | None:
        some = self.auto(name, critical=False)
        return some if isinstance(some, guard) else None

    def manual(self, name: str, *, critical: bool = True) -> Any | None:
        item = self.__get(name)
        if item is None or not item.visible:
            if not critical:
                return None
            logging.warning("%s: Attempting to get `%s` which is out of context",
                            utils.name(self), name)
            raise RuntimeError(f"Name `{name}` out of context")
        return item.value

    def union(self, context: "Context", *, override: bool = False) -> "Context":
        storage = self.__storage.copy()
        other = context.__storage.copy()
        if intersected := storage.keys() & other.keys():
            if not override:
                logging.error("%s: Attempting to override intersected names when no override allowed: %s",
                              utils.name(self), intersected)
                raise RuntimeError(f"Unable to union the context: one or several names are intersected: {intersected}")
            if any(not storage[name].visible for name in intersected):
                logging.error("%s: Attempting to override intersected names when some of names are invisible: %s",
                              utils.name(self), intersected)
                raise RuntimeError(f"Unable to union the context: one or several names are intersected: {intersected}."
                                   " Note: overriding is not allowed for invisible items")
        return Context(**(storage | other))

    def unwrap(self, name: str, guard: Type[T]) -> T:
        some = self.checked(name, guard)
        if some is None:
            logging.warning("%s: Attempting to unwrap `%s` with type %s. `%s` is not instance of %s",
                            utils.name(self), name, utils.name(guard), name, utils.name(guard))
            raise RuntimeError(f"Unable to unwrap {name} with guard type {guard} from context")
        return some

    def with_object(self, some: Any, *, name: str | None = None, visible: bool = True) -> "Context":
        key = name if name is not None else utils.name(some)
        item = self.__get(key, respectful=False)
        if item is not None:
            logging.warning("%s: Attempting to set `%s` with name %s. Such name already exists",
                            utils.name(self), utils.name(some), name)
            raise RuntimeError(f"Object with the same name already exits with visible state `{item.visible}`")
        self.__storage[key] = ContextItem(visible, some)
        return self
