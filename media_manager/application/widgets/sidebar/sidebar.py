import logging

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QVBoxLayout, QWidget

from media_manager.application.api.events import EventPool
from media_manager.application.api.events.module import WidgetInstalledEvent

from .listeners import SideBarWidgetFocusListener
from .other import OtherWidgets
from .system import SystemWidgets
from .widget import SideBarWidget

from ..abc import SupportableModule


class SideBar(QWidget):
    def __init__(self, events: EventPool):
        super().__init__()
        self.events = events
        self.__modules: dict[str, tuple[SupportableModule, SideBarWidget]] = {}
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

    def append(self, module: SupportableModule):
        id = module.meta().id()
        if id in self.__modules:
            logging.error("%s: Attempting to add already existed module widget: %s (%s)",
                          type(self).__name__, module.meta().name(), module.meta().version())
            return

        bar_widget = SideBarWidget(module.widget().widget())
        if module.widget().type() == "System":
            self.__system_widgets.add(module, bar_widget)
        else:
            self.__other_widgets.add(module, bar_widget)

        self.__modules[id] = module, bar_widget
        # Event listeners
        module.widget().events().subscribe(SideBarWidgetFocusListener(self, bar_widget))
        # Event announces
        module.widget().events().announce(WidgetInstalledEvent(module))

    def items(self) -> list[tuple[SupportableModule, SideBarWidget]]:
        return list(self.__modules.values())
