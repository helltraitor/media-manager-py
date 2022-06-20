from weakref import ReferenceType

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QLabel, QVBoxLayout

from media_manager.application.api.context import Context
from media_manager.application.api.module.components import CWindow
from media_manager.application.api.module.components.window.abc import Window
from media_manager.application.api.module.features import FWindow


class AboutWindow(Window):
    def __init__(self, component: ReferenceType[CWindow]):
        super().__init__(component)
        self.__about_title = QLabel()
        self.__program_title = QLabel()
        self.__layout = QVBoxLayout(self)
        self.__setup()

    def __setup(self):
        self.__layout.setContentsMargins(6, 6, 6, 6)
        # Labels
        self.__about_title.setText("About")
        self.__layout.addWidget(self.__about_title, alignment=Qt.AlignLeft)

        self.__program_title.setText("Media manager")
        self.__layout.addWidget(self.__program_title, alignment=Qt.AlignLeft)


class CAboutWindow(CWindow):
    def __init__(self, context: Context):
        super().__init__(context)
        self.__window = AboutWindow(ReferenceType(self))

    def window(self) -> Window:
        return self.__window
