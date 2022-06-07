import logging

from typing import Iterator

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QVBoxLayout, QSizePolicy, QWidget

from .widget import SideBarWidget


class SystemWidgets(QWidget):
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
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)

    def widgets(self) -> Iterator[SideBarWidget]:
        return iter(self.__widgets)

    def widget_add(self, bar_widget: SideBarWidget):
        if bar_widget in self.__widgets:
            logging.warning(
                f'{type(self).__name__}: Attempting to add already added module widget: {type(bar_widget.module())}')
            return

        self.__widgets.append(bar_widget)
        self.__layout.addWidget(bar_widget, alignment=Qt.AlignBottom)
