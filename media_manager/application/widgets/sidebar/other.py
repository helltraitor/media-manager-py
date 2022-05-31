import logging

from typing import Iterator

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QVBoxLayout, QSizePolicy, QWidget

from media_manager.application.api.module import ModuleWidget

from .widget import SideBarWidget


class OtherWidgets(QWidget):
    def __init__(self):
        super().__init__()
        self.__widgets: list[SideBarWidget] = []
        self.__layout = QVBoxLayout(self)
        # Setup
        self.__setup()

    def __setup(self):
        # Layout
        self.__layout.setContentsMargins(0, 0, 0, 0)
        # Self
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)

    def widgets(self) -> Iterator[SideBarWidget]:
        return iter(self.__widgets)

    def widget_add(self, module: ModuleWidget):
        if self.widget_exists(module):
            logging.warning(f'{type(self).__name__}: Attempting to add already added module widget: {type(module)}')
            return

        widget = SideBarWidget(module)
        self.__widgets.append(widget)
        self.__layout.addWidget(widget, alignment=Qt.AlignBottom)

    def widget_exists(self, module: ModuleWidget) -> bool:
        return module in map(SideBarWidget.module, self.__widgets)

