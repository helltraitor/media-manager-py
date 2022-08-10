from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QHBoxLayout, QWidget

from media_manager.application.constants import APPLICATION_ICON, APPLICATION_NAME
from media_manager.application.api.events import EventPool

from .abc import SupportableModule
from .listeners import ModuleFocusListener
from .main import MainWidget
from .sidebar import SideBar


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.events = EventPool()
        self.__icon = QIcon(str(APPLICATION_ICON))

        self.__layout = QHBoxLayout(self)
        self.__side = SideBar(self.events)
        self.__main = MainWidget(self.events)
        self.__setup()

    def __setup(self):
        # Layout
        self.__layout.setAlignment(Qt.AlignLeft)
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__layout.addWidget(self.__side)
        self.__layout.addWidget(self.__main)
        # Window
        self.setWindowIcon(self.__icon)
        self.setWindowTitle(APPLICATION_NAME)
        self.setGeometry(*max(self.geometry().getCoords(), (50, 50, 200, 200), key=sum))

    def append(self, module: SupportableModule):
        module.widget().events().subscribe(ModuleFocusListener(self.__main))
        self.__main.append(module)
        self.__side.append(module)
