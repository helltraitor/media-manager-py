import logging

from abc import ABC, abstractmethod

from PySide2.QtCore import QEvent
from PySide2.QtWidgets import QWidget

from media_manager.application.callbacks import Callback


class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.__callbacks: dict[str, Callback] = {}

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


class ModuleWidget(ABC):
    @abstractmethod
    def widget(self) -> Widget:
        pass
