from pathlib import Path
from weakref import ReferenceType

from media_manager.application.api.context import Context
from media_manager.application.api.events import EventPool

from .abc import Widget
from .default import DefaultWidget

from ..abc import Component


class CWidget(Component):
    def __init__(self, context: Context):
        super().__init__(context)
        self.__events = EventPool()
        self.__type = context.checked("type", str) or "Other"

    def events(self) -> EventPool:
        return self.__events

    def type(self) -> str:
        return self.__type

    def widget(self) -> Widget:
        raise NotImplementedError("This method must be implemented in subclass")


class CDefaultWidget(CWidget):
    ICON = str(Path(__file__).parent.parent.parent.parent.parent.parent / "resources" / "carol-liao-solve-icon.svg")

    def __init__(self, context: Context):
        super().__init__(context)
        self.__icon = context.checked("icon", str) or self.ICON
        self.__title = context.checked("title", str) or "Unknown"
        self.__widget = DefaultWidget(ReferenceType(self))

    def icon(self) -> str:
        return self.__icon

    def title(self) -> str:
        return self.__title

    def widget(self) -> DefaultWidget:
        return self.__widget
