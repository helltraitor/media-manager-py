import logging

from PySide2.QtWidgets import QWidget, QStackedLayout

from media_manager.application.api.events import EventPool

from .layer import MainWidgetLayer
from ..abc import SupportableModule


class MainWidget(QWidget):
    def __init__(self, events: EventPool):
        super().__init__()
        self.events = events
        self.__current: SupportableModule | None = None
        self.__windows: dict[str, tuple[SupportableModule, MainWidgetLayer]] = {}
        self.__layout = QStackedLayout(self)
        self.__setup()

    def __setup(self):
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__layout.addWidget(QWidget())

    def append(self, module: SupportableModule):
        id = module.meta().id()
        if id in self.__windows:
            logging.error("%s: Attempting to add already existed module widget: %s (%s)",
                          type(self).__name__, module.meta().name(), module.meta().version())
            return

        layer = MainWidgetLayer(module.window().window())
        self.__layout.addWidget(layer)
        self.__windows[id] = module, layer
        self.choose(self.__current)

    def choose(self, module: SupportableModule | None):
        if module is None:
            self.__layout.setCurrentIndex(0)
            return

        id = module.meta().id()
        if id not in self.__windows:
            logging.warning('%s: Attempting to show non existing module window',
                            type(self).__name__)
        self.__current = module
        self.__layout.setCurrentWidget(self.__windows[id][-1])

    def list(self) -> list[tuple[SupportableModule, MainWidgetLayer]]:
        return list(self.__windows.values())
