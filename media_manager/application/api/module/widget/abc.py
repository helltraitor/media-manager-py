import logging

from abc import ABC, abstractmethod

from PySide2.QtCore import QEvent
from PySide2.QtWidgets import QWidget

from media_manager.application.callbacks import Callback


# class ModuleWidget(ABC, QWidget):
class ModuleWidget(QWidget):
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

    @abstractmethod
    def module_icon(self) -> str:
        pass

    @abstractmethod
    def module_title(self) -> str:
        pass

    @abstractmethod
    def widget_selected(self) -> bool:
        pass

    @abstractmethod
    def widget_reset_selection(self):
        pass
