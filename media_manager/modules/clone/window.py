from PySide2.QtCore import Qt
from PySide2.QtWidgets import QPushButton, QLabel, QVBoxLayout, QWidget

from media_manager.application.api.messages import Message
from media_manager.application.api.module import ModuleWindow


class Window(QWidget):
    def __init__(self, window: ModuleWindow, id_: str):
        super().__init__()
        self.__window = window
        self.__id = id_
        self.__clone_title = QLabel(f'Clone #{self.__id}')
        self.__clone_settings = QPushButton("Settings")
        self.__layout = QVBoxLayout(self)
        self.__setup()

    def __setup(self):
        self.__layout.setContentsMargins(6, 6, 6, 6)
        self.__layout.addWidget(self.__clone_title, alignment=Qt.AlignLeft)
        self.__layout.addSpacing(6)
        self.__layout.addWidget(self.__clone_settings, alignment=Qt.AlignLeft)
        # Button
        self.__clone_settings.clicked.connect(
            lambda: self.__window.module().client().send(
                {"name": "Application"}, Message({"text": "Hello, Messages!"})))
