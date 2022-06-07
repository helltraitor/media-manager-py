from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .sidebar import SideBar
    from .widget import SideBarWidget

from typing import Type

from media_manager.application.api.events import Event, EventListener
from media_manager.application.api.events.module import (
    WidgetFocusedEvent,
    WidgetUnfocusedEvent,
)


class SideBarWidgetFocusListener(EventListener):
    def __init__(self, sidebar: "SideBar", target: "SideBarWidget"):
        self.__sidebar = sidebar
        self.__target = target

    def events(self) -> frozenset[Type[Event]]:
        return frozenset((WidgetFocusedEvent,))

    def handle(self, event: Event):
        if not isinstance(event, WidgetFocusedEvent):
            return
        for (module, bar_widget) in self.__sidebar.items():
            if bar_widget is self.__target:
                self.__sidebar.events.announce(WidgetFocusedEvent(module))
                continue
            module.widget().events.announce(WidgetUnfocusedEvent(module))
