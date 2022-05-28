from PySide2.QtCore import QEvent
from PySide2.QtWidgets import QWidget

from media_manager.application.api.events import Event


class GuiEvent(Event):
    def __init__(self, reason: QEvent, target: QWidget):
        self.__reason = reason
        self.__target = target

    @property
    def reason(self):
        return self.__reason

    @property
    def target(self):
        return self.__target


class PaintEvent(GuiEvent):
    pass
