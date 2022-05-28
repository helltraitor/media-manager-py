from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from .core import ModuleDefaultWidget

from PySide2.QtCore import QEvent

from media_manager.application.api.events import Event, EventListener
from media_manager.application.api.events.gui import GuiEvent
from media_manager.application.api.events.module import WidgetFocusedEvent, WidgetUnfocusedEvent

from .painters import (
    ModuleWidgetGrayBackgroundPainter, ModuleWidgetNoneBackgroundPainter, ModuleWidgetWhiteBackgroundPainter
)


class DefaultBackgroundListener(EventListener):
    def __init__(self, module: "ModuleDefaultWidget"):
        super().__init__()
        self.__module = module
        self.__widget = module.widget()

    def events(self) -> frozenset[Type[Event]]:
        return frozenset((GuiEvent, WidgetFocusedEvent, WidgetUnfocusedEvent))

    def handle(self, event: Event):
        if isinstance(event, WidgetUnfocusedEvent):
            self.__widget.painter = ModuleWidgetNoneBackgroundPainter
        elif isinstance(event, WidgetFocusedEvent):
            self.__widget.painter = ModuleWidgetWhiteBackgroundPainter
        elif isinstance(event, GuiEvent) and event.target is self.__widget:
            if self.__widget.painter is not ModuleWidgetWhiteBackgroundPainter:
                if event.reason.type() == QEvent.Enter:
                    self.__module.widget().painter = ModuleWidgetGrayBackgroundPainter
                elif event.reason.type() == QEvent.Leave:
                    self.__module.widget().painter = ModuleWidgetNoneBackgroundPainter
        self.__module.widget().update()


class DefaultBackgroundPaintEventListener(EventListener):
    def __init__(self, module: "ModuleDefaultWidget"):
        super().__init__()
        self.__module = module

    def events(self) -> frozenset[Type[Event]]:
        return frozenset((GuiEvent,))

    def handle(self, event: Event):
        if isinstance(event, GuiEvent) and event.target is self.__module.widget():
            if event.reason.type() == QEvent.Paint:
                self.__module.widget().painter.paint(self.__module.widget())
