import logging
from weakref import ReferenceType

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QPushButton, QLabel, QVBoxLayout

from media_manager.application.api.context import Context
from media_manager.application.api.messages import CallbackMessage, SignableMessage, Target
from media_manager.application.api.module import Module
from media_manager.application.api.module.components import CMessageClient, CWindow
from media_manager.application.api.module.components.window.abc import Window
from media_manager.application.api.module.features import FMessages, FWindow


class CloneWindow(Window):
    def __init__(self, component: ReferenceType[CWindow]):
        super().__init__(component)
        self.__client: CMessageClient | None = None
        self.__clone_title = QLabel()
        self.__clone_up = QPushButton("^^^")
        self.__clone_value = QLabel("0")
        self.__clone_down = QPushButton("vvv")
        self.__layout = QVBoxLayout(self)
        self.__setup()

    def __setup(self):
        # GUI
        self.__clone_down.setAutoRepeat(True)
        self.__clone_up.setAutoRepeat(True)
        #
        self.__layout.setContentsMargins(6, 6, 6, 6)
        self.__layout.addWidget(self.__clone_title, alignment=Qt.AlignTop)
        self.__layout.addSpacing(6)
        self.__layout.addWidget(self.__clone_up, alignment=Qt.AlignTop)
        self.__layout.addWidget(self.__clone_value, alignment=Qt.AlignTop)
        self.__layout.addWidget(self.__clone_down, alignment=Qt.AlignTop)

    def link_stage_setup(self, name:str, id: str, client: CMessageClient):
        self.__clone_title.setText(f"{name} [{id}]")

        self.__client = client
        self.__client.client().send(
            Target("Settings"),
            SignableMessage({"action": "set", "key": "counter", "value": "0"}))

        self.__clone_up.clicked.connect(lambda: self.change_value(1))
        self.__clone_down.clicked.connect(lambda: self.change_value(-1))

    def change_value(self, delta: int):
        if self.__client is None:
            return

        client = self.__client.client()
        client.send(Target("Settings"), CallbackMessage(  # GET VALUE FROM STORAGE
            {"action": "get", "key": "counter"},
            lambda reply: client.send(Target("Settings"), CallbackMessage(  # CHANGE GOT VALUE
                {"action": "set", "key": "counter", "value": str(int(reply.content().get("value", "0")) + delta)},
                lambda _: client.send(Target("Settings"), CallbackMessage(  # PUT IT IN THE LABEL
                    {"action": "get", "key": "counter"},
                    lambda reply: self.__clone_value.setText(reply.content().get("value", "ERROR"))))))))


class CCloneWindow(CWindow):
    def __init__(self, context: Context):
        super().__init__(context)
        self.__id = context.unwrap("id", str)
        self.__name = context.unwrap("name", str)

        self.__context = context
        self.__window = CloneWindow(ReferenceType(self))

    def id(self) -> str:
        return self.__context.unwrap('id', str)

    def link(self, module: Module):
        super().link(module)
        client = module.components().get_unwrap(FMessages, CMessageClient)
        self.__window.link_stage_setup(self.__name, self.__id, client)

    def window(self) -> Window:
        return self.__window
