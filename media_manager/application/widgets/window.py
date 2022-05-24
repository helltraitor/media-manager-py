from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QHBoxLayout, QWidget

from media_manager.application.constants import APPLICATION_ICON, APPLICATION_NAME

from .main import MainWidget
from .sidebar import SideBar


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.icon = QIcon(APPLICATION_ICON)

        self.h_layout = QHBoxLayout(self)
        self.side_bar = SideBar()
        self.main = MainWidget()
        self.__setup()

    def __setup(self):
        # Layout
        self.h_layout.setAlignment(Qt.AlignLeft)
        self.h_layout.setContentsMargins(0, 0, 0, 0)
        self.h_layout.addWidget(self.side_bar)
        # Window
        self.setWindowIcon(self.icon)
        self.setWindowTitle(APPLICATION_NAME)
        self.setGeometry(*max(self.geometry().getCoords(), (50, 50, 200, 200), key=sum))
