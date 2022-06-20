from media_manager.application.api.context import Context
from media_manager.application.api.events import EventPool

from ..abc import Component

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .abc import Window


class CWindow(Component):
    def __init__(self, context: Context):
        super().__init__(context)
        self.__events = EventPool()

    def events(self) -> EventPool:
        return self.__events

    def window(self) -> "Window":
        raise NotImplementedError("This method must be implemented in subclass")
