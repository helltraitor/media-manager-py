from PySide2.QtCore import Qt
from PySide2.QtWidgets import QLabel, QListWidget, QSizePolicy, QVBoxLayout, QWidget

from .storage import Storage


class TableWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.__storage = Storage()
        self.__setup()

    def __setup(self):
        self.__storage.subscribe("set", self.refill)
        self.__storage.subscribe("delete", self.refill)
        self.refill()

    def refill(self):
        self.clear()
        self.addItems(tuple(f"`{key}` :: `{value}`" for key, value in self.__storage.all().items()))


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.__title = QLabel()
        self.__table = TableWidget()
        self.__layout = QVBoxLayout(self)
        self.__setup()

    def __setup(self):
        self.__layout.setContentsMargins(6, 6, 6, 6)
        # Label
        font = self.__title.font()
        font.setPointSize(18)
        self.__title.setText("Settings")
        self.__title.setFont(font)
        self.__title.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        self.__layout.addWidget(self.__title, alignment=(Qt.AlignLeft | Qt.AlignTop))
        # Table
        self.__table.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.__layout.addSpacing(6)
        self.__layout.addWidget(self.__table)
