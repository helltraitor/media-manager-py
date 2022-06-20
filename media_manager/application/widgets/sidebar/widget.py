from PySide2.QtCore import Qt
from PySide2.QtWidgets import QVBoxLayout, QWidget

from media_manager.application.api.module.components.widget.abc import Widget


class SideBarWidget(QWidget):
    def __init__(self, widget: Widget):
        super().__init__()
        self.__layout = QVBoxLayout(self)
        self.__widget = widget
        # Setup
        self.__setup()

    def __setup(self):
        # Layout
        self.__layout.setContentsMargins(6, 6, 6, 6)
        self.__layout.addWidget(self.__widget, alignment=Qt.AlignCenter)
        # Widget
        self.__widget.setFixedSize(72, 72)
