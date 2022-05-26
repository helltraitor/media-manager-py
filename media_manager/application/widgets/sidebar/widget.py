from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QVBoxLayout

from media_manager.application.api.module.widget import Widget


class SideBarWidget(QWidget):
    def __init__(self, widget: Widget):
        super().__init__()
        self.__layout = QVBoxLayout()
        self.__widget = widget
        self.__setup()

    def __setup(self):
        # Layout
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__layout.addWidget(self.__widget, alignment=Qt.AlignCenter)
        # Self
        self.setFixedSize(72, 72)
