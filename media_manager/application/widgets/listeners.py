from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .main import MainWidget

from typing import Type

from media_manager.application.api.events import Event, EventListener
from media_manager.application.api.events.module import WidgetFocusedEvent


class ModuleFocusListener(EventListener):
    def __init__(self, main: "MainWidget"):
        self.__main = main

    def events(self) -> frozenset[Type[Event]]:
        return frozenset((WidgetFocusedEvent,))

    def handle(self, event: Event):
        if not isinstance(event, WidgetFocusedEvent):
            return
        for module, _ in self.__main.list():
            if module is event.module():
                self.__main.choose(module)
