from PySide2.QtCore import Qt
from PySide2.QtWidgets import QLabel, QVBoxLayout, QWidget


class Window(QWidget):
    def __init__(self):
        super().__init__()
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
