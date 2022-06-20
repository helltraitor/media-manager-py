from weakref import ReferenceType

from PySide2.QtCore import QEvent
from PySide2.QtWidgets import QWidget

from media_manager.application.api.events.gui import GuiEvent

from .component import CWindow


class Window(QWidget):
    def __init__(self, component: ReferenceType[CWindow]):
        super().__init__()
        self.__component = component

    def component(self) -> CWindow:
        component = self.__component()
        if component is not None:
            return component
        raise RuntimeError("CWidget is None")

    def event(self, event: QEvent) -> bool:
        self.component().events().announce(GuiEvent(event, self))
        return super().event(event)
