from PySide2.QtCore import Qt
from PySide2.QtWidgets import QVBoxLayout, QWidget

from media_manager.application.api.module.widget import ModuleWidget


class SideBarWidget(QWidget):
    def __init__(self, module: ModuleWidget):
        super().__init__()
        self.__layout = QVBoxLayout(self)
        self.__module = module
        self.__widget = module.widget()
        # Setup
        self.__setup()

    def __setup(self):
        # Layout
        self.__layout.setContentsMargins(6, 6, 6, 6)
        self.__layout.addWidget(self.__widget, alignment=Qt.AlignCenter)
        # Widget
        self.__widget.setFixedSize(72, 72)

    def module(self) -> ModuleWidget:
        return self.__module
