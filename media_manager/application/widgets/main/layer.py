import logging

from PySide2.QtCore import QEvent
from PySide2.QtWidgets import QWidget, QLayout

from media_manager.application.api.module.window import ModuleWindow


class MainWidgetLayer(QWidget):
    def __init__(self, window: ModuleWindow):
        super().__init__(self)
        self.__container = QLayout(self)
        self.__window = window

    def __setup(self):
        # Layout
        self.__container.setContentsMargins(0, 0, 0, 0)
        self.__container.addWidget(self.__window.window())

    def event(self, event: QEvent) -> bool:
        for callback in self.__callbacks.values():
            callback.call_on(event)
        return False
