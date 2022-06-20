import logging

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QVBoxLayout, QSizePolicy, QWidget

from .widget import SideBarWidget
from ..abc import SupportableModule


class SystemWidgets(QWidget):
    def __init__(self):
        super().__init__()
        self.__widgets: dict[str, SideBarWidget] = {}
        self.__layout = QVBoxLayout(self)
        # Setup
        self.__setup()

    def __setup(self):
        # Layout
        self.__layout.setContentsMargins(0, 0, 0, 0)
        # Self
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)

    def add(self, module: SupportableModule, widget: SideBarWidget):
        id = module.meta().id()
        if id in self.__widgets:
            logging.warning("%s: Attempting to add already existed module widget: %s (%s)",
                            type(self).__name__, module.meta().name(), module.meta().id())
            return
        self.__widgets[id] = widget
        self.__layout.addWidget(widget, alignment=Qt.AlignBottom)

    def list(self) -> list[SideBarWidget]:
        return list(self.__widgets.values())
