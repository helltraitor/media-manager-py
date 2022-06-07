import logging

from collections.abc import Iterable

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QVBoxLayout, QWidget

from media_manager.application.api.events import EventPool
from media_manager.application.api.events.module import (
    WidgetInstalledEvent,
    WidgetUninstalledEvent
)

from media_manager.application.api.module import Module

from .listeners import SideBarWidgetFocusListener
from .other import OtherWidgets
from .system import SystemWidgets
from .widget import SideBarWidget


class SideBar(QWidget):
    def __init__(self, events: EventPool):
        super().__init__()
        self.events = events
        self.__modules: dict[str, tuple[Module, SideBarWidget]] = {}
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

    def items(self) -> Iterable[tuple[Module, SideBarWidget]]:
        return self.__modules.values()

    def module_add(self, module: Module):
        if module.id() in self.__modules:
            logging.warning(f'{type(self).__name__}: Attempting to add already added module widget: {type(module)}')
            return

        bar_widget = SideBarWidget(module.widget())
        if module.widget().type() == "System":
            self.__system_widgets.widget_add(bar_widget)
        else:
            self.__other_widgets.widget_add(bar_widget)
        self.__modules[module.id()] = (module, bar_widget)

        # Event listeners
        module.widget().events.subscribe(SideBarWidgetFocusListener(self, bar_widget))
        # Event announces
        module.widget().events.announce(WidgetInstalledEvent(module.widget()))
