from PySide2.QtCore import Qt
from PySide2.QtWidgets import QLabel, QVBoxLayout, QWidget


class Window(QWidget):
    def __init__(self, id_: str):
        super().__init__()
        self.__id = id_
        self.__clone_title = QLabel()
        self.__layout = QVBoxLayout(self)
        self.__setup()

    def __setup(self):
        self.__layout.setContentsMargins(6, 6, 6, 6)
        # Labels
        self.__clone_title.setText(f'Clone #{self.__id}')
        self.__layout.addWidget(self.__clone_title, alignment=Qt.AlignLeft)
