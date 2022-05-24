import logging

from PySide2.QtCore import QEvent
from PySide2.QtWidgets import QWidget, QLayout

from media_manager.application.api import ModuleWindow
from media_manager.application.callbacks import Callback


class MainWidgetLayer(QWidget):
    def __init__(self, window: ModuleWindow):
        super().__init__(self)
        self.__callbacks: dict[str, Callback] = {}
        self.__container = QLayout(self)
        self.__window = window

    def __setup(self):
        # Layout
        self.__container.setContentsMargins(0, 0, 0, 0)
        self.__container.addWidget(self.__window.window())
        self.__setup_callbacks()

    def __setup_callbacks(self):
        pass

    def event(self, event: QEvent) -> bool:
        for callback in self.__callbacks.values():
            callback.call_on(event)
        return False

    def callback_set(self, key: str, callback: Callback):
        self.__callbacks[key] = callback

    def callback_remove(self, key: str):
        callback = self.__callbacks.pop(key, None)
        if callback is None:
            logging.warning(f'{type(self).__name__}: Attempting to remove non-existing callback')
