from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from media_manager.application.api.events.control import EventPool

from .listener import EventListener


class EventSubscription:
    def __init__(self, listener: EventListener, pool: "EventPool"):
        self.__cancelled = False
        self.__listener = listener
        self.__pool = pool

    def cancel(self):
        if self.cancelled():
            return
        self.__cancelled = True
        self.__pool.unsubscribe(self)

    def cancelled(self) -> bool:
        return self.__cancelled

    @property
    def listener(self) -> EventListener:
        return self.__listener
