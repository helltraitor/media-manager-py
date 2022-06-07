from PySide2.QtCore import Qt
from PySide2.QtWidgets import QLabel, QVBoxLayout, QWidget


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.__settings_title = QLabel()
        self.__layout = QVBoxLayout(self)
        self.__setup()

    def __setup(self):
        self.__layout.setContentsMargins(6, 6, 6, 6)
        # Labels
        self.__settings_title.setText("Settings")
        self.__layout.addWidget(self.__settings_title, alignment=Qt.AlignLeft)
