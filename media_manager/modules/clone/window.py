from PySide2.QtCore import Qt
from PySide2.QtWidgets import QPushButton, QLabel, QVBoxLayout, QWidget

from media_manager.application.api.messages import Message, CallbackMessage
from media_manager.application.api.module import ModuleWindow


class Window(QWidget):
    def __init__(self, window: ModuleWindow, id_: str):
        super().__init__()
        self.__window = window
        self.__id = id_
        self.__clone_title = QLabel(f'Clone #{self.__id}')
        self.__clone_up = QPushButton("^^^")
        self.__clone_value = QLabel("0")
        self.__clone_down = QPushButton("vvv")
        self.__layout = QVBoxLayout(self)
        self.__setup()

    def __setup(self):
        self.__layout.setContentsMargins(6, 6, 6, 6)
        self.__layout.addWidget(self.__clone_title, alignment=Qt.AlignTop)
        self.__layout.addSpacing(6)
        self.__layout.addWidget(self.__clone_up, alignment=Qt.AlignTop)
        self.__layout.addWidget(self.__clone_value, alignment=Qt.AlignTop)
        self.__layout.addWidget(self.__clone_down, alignment=Qt.AlignTop)
        # INIT SETTING
        client = self.__window.module().client()
        client.send({"name": "Settings"}, Message({"action": "set", "key": f"{self.__id}-value", "value": "0"}))
        # BUTTON
        self.__clone_up.setAutoRepeat(True)
        self.__clone_up.clicked.connect(
            lambda: change_value(client, self.__id, int(self.__clone_value.text()) + 1) or fetch_value(client, self.__id, self.__clone_value))
        self.__clone_down.setAutoRepeat(True)
        self.__clone_down.clicked.connect(
            lambda: change_value(client, self.__id, int(self.__clone_value.text()) - 1) or fetch_value(client, self.__id, self.__clone_value))


def change_value(client, id, value):
    client.send({"name": "Settings"},
                Message({"action": "set", "key": f"{id}-value", "value": str(value)}))


def fetch_value(client, id, label):
    client.send({"name": "Settings"}, CallbackMessage(
                lambda reply: label.setText(reply.content().get("value", label.text())), {
                    "action": "get", "key": f"{id}-value"}))
