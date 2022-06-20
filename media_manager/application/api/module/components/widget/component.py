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

    def events(self) -> EventPool:
        return self.__events

    def type(self) -> str:
        return "Other"

    def widget(self) -> Widget:
        raise NotImplementedError("This method must be implemented in subclass")


class CDefaultWidget(CWidget):
    def __init__(self, context: Context):
        super().__init__(context)
        self.__widget = DefaultWidget(ReferenceType(self))

    def icon(self) -> str:
        return str(Path(__file__).parent.parent.parent.parent.parent.parent / "resources" / "carol-liao-solve-icon.svg")

    def title(self) -> str:
        raise NotImplementedError("This method must be implemented in subclass")

    def widget(self) -> DefaultWidget:
        return self.__widget
