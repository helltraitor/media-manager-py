import logging

from pathlib import Path

from PySide2.QtCore import QTimer
from PySide2.QtWidgets import QApplication

from media_manager.application.api.context import Context
from media_manager.application.api.deferred import DeferredPool
from media_manager.application.api.messages import MessageServer, MessageClient, Message, Reply
from media_manager.application.widgets.window import SupportableModule, Window
from media_manager.application.modules import Keeper, Loader


class ApplicationClient(MessageClient):
    def __init__(self, keeper: Keeper):
        super().__init__("Application", {
            "name": "Application"
        })
        self.__keeper = keeper

    def accepts(self, credits: dict[str, str]) -> bool:
        return self.__keeper.contains(id=credits.get("id", ""))

    def receive(self, message: Message) -> Reply:
        logging.info(message.content())
        return Reply(message.content())


class Application(QApplication):
    def __init__(self, location: Path):
        super().__init__()
        self.__server_timer = QTimer(self)
        self.__deferred_timer = QTimer(self)
        #
        self.context = Context()
        self.keeper = Keeper()
        self.loader = Loader()
        self.window = Window()
        #
        self.__setup(location)

    def __setup(self, location: Path):
        deferred_pool = DeferredPool()
        self.__deferred_timer.timeout.connect(deferred_pool.process)
        self.context.with_object(deferred_pool, visible=False)

        message_server = MessageServer()
        self.__server_timer.timeout.connect(message_server.process)
        self.context.with_object(message_server, visible=False)

        modules_location = location / "media_manager" / "modules"
        for module in self.loader.load_from(modules_location, context=self.context):
            self.keeper.append(module)
            if isinstance(module, SupportableModule):
                self.window.append(module)

        # Anonymous application client
        client = ApplicationClient(self.keeper)
        client.connect(message_server)

    def start(self) -> int:
        self.__server_timer.start(0)
        self.__deferred_timer.start(25)
        self.window.show()
        return self.exec_()
