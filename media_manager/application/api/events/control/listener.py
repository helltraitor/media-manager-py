from abc import ABC, abstractmethod
from typing import Type

from media_manager.application.api.events.abc import Event


class EventListener(ABC):
    @abstractmethod
    def events(self) -> frozenset[Type[Event]]:
        pass

    @abstractmethod
    def handle(self, event: Event):
        pass
