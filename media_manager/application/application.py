import logging

from pathlib import Path

from PySide2.QtCore import QTimer
from PySide2.QtWidgets import QApplication

from media_manager.application.api.context import Context
from media_manager.application.api.deferred import DeferredPool
from media_manager.application.api.messages import MessageServer
from media_manager.application.widgets.window import SupportableModule, Window
from media_manager.application.modules import Keeper, Loader


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

    def start(self) -> int:
        self.__server_timer.start(0)
        self.__deferred_timer.start(25)
        self.window.show()
        return self.exec_()
