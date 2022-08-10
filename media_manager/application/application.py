import logging

from pathlib import Path

from PySide2.QtCore import QTimer
from PySide2.QtWidgets import QApplication

from media_manager.application.api.context import Context
from media_manager.application.api.deferred import DeferredPool
from media_manager.application.api.messages import MessageServer
from media_manager.application.modules import Manager, Loader


class Application(QApplication):
    def __init__(self):
        super().__init__()
        self.__server_timer = QTimer(self)
        self.__deferred_timer = QTimer(self)
        #
        self.context = Context()
        self.manager = Manager(self.context)
        #
        self.__setup()

    def __setup(self):
        self.aboutToQuit.connect(self.manager.unload)

        deferred_pool = DeferredPool()
        self.__deferred_timer.timeout.connect(deferred_pool.process)
        self.context.with_object(deferred_pool, visible=False)

        message_server = MessageServer()
        self.__server_timer.timeout.connect(message_server.process)
        self.context.with_object(message_server, visible=False)

    def start(self) -> int:
        self.__server_timer.start(0)
        self.__deferred_timer.start(25)
        self.manager.load()
        self.manager.window.show()
        return self.exec_()
