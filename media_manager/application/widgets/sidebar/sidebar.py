import logging

from typing import Iterator

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QVBoxLayout, QWidget

from media_manager.application.api.events.module import (
    WidgetInstalledEvent,
    WidgetUninstalledEvent
)

from media_manager.application.api.module import ModuleWidget

from .listeners import SideBarWidgetFocusListener
from .widget import SideBarWidget


from PySide2 import QtWidgets
from PySide2 import QtCore


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
        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Fixed))

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
        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed))

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


class SideBar(QWidget):
    def __init__(self):
        super().__init__()
        self.__widgets: list[SideBarWidget] = []
        # GUI
        self.__other_widgets = OtherWidgets()
        self.__system_widgets = SystemWidgets()
        self.__layout = QVBoxLayout(self)
        # Setup
        self.__setup()

    def __setup(self):
        # Layout
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__layout.addWidget(self.__other_widgets, alignment=Qt.AlignTop)
        self.__layout.addSpacing(84)
        self.__layout.addWidget(self.__system_widgets, alignment=Qt.AlignBottom)
        # Self
        self.setFixedWidth(84)

    def widgets(self) -> Iterator[SideBarWidget]:
        return iter(self.__widgets)

    def widget_add(self, module: ModuleWidget):
        if self.widget_exists(module):
            logging.warning(f'{type(self).__name__}: Attempting to add already added module widget: {type(module)}')
            return

        widget = SideBarWidget(module)
        self.__widgets.append(widget)

        if module.type() == "System":
            self.__system_widgets.widget_add(module)
        else:
            self.__other_widgets.widget_add(module)

        # Event listeners
        module.events.subscribe(SideBarWidgetFocusListener(self, widget))
        # Event announces
        module.events.announce(WidgetInstalledEvent(module))

    def widget_exists(self, module: ModuleWidget) -> bool:
        return module in map(SideBarWidget.module, self.__widgets)
