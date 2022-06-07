import logging

from collections.abc import Iterable

from PySide2.QtWidgets import QWidget, QStackedLayout

from media_manager.application.api.events import EventPool
from media_manager.application.api.module import Module

from .layer import MainWidgetLayer


class MainWidget(QWidget):
    def __init__(self, events: EventPool):
        super().__init__()
        self.events = events
        self.__current: Module | None = None
        self.__modules: dict[str, tuple[Module, MainWidgetLayer]] = {}
        self.__layout = QStackedLayout(self)
        self.__setup()

    def __setup(self):
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__layout.addWidget(QWidget())

    def modules(self) -> Iterable[tuple[Module, MainWidgetLayer]]:
        return self.__modules.values()

    def module_add(self, module: Module):
        if module.id() in self.__modules:
            logging.warning(f'{type(self).__name__}: Attempting to add already added module window')
            return

        layer = MainWidgetLayer(module.window())
        self.__layout.addWidget(layer)
        self.__modules[module.id()] = (module, layer)

        self.module_show(self.__current)

    def module_show(self, module: Module | None):
        if module is None:
            self.__layout.setCurrentIndex(0)
            return

        if module.id() not in self.__modules:
            logging.warning(f'{type(self).__name__}: Attempting to show non existing module window')
            return

        self.__current = module
        layer = self.__modules[module.id()][-1]
        self.__layout.setCurrentWidget(layer)
