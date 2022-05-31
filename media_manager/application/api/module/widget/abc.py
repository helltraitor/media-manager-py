from abc import ABC, abstractmethod

from PySide2.QtCore import QEvent
from PySide2.QtWidgets import QWidget

from media_manager.application.api.events import EventPool
from media_manager.application.api.events.gui import GuiEvent


class Widget(QWidget):
    def __init__(self, module: "ModuleWidget"):
        super().__init__()
        self.__module = module

    @property
    def module(self):
        return self.__module

    def event(self, event: QEvent) -> bool:
        # Qt event must be processed first
        q_result = super().event(event)
        self.module.events.announce(GuiEvent(event, self))
        return q_result


class ModuleWidget(ABC):
    def __init__(self):
        # Safety for sharing
        self.events = EventPool()

    @abstractmethod
    def widget(self) -> Widget:
        pass

    def type(self) -> str:
        return "Other"
