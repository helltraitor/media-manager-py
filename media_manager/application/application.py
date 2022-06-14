from pathlib import Path

from PySide2.QtWidgets import QApplication

from media_manager.application.api.messages import MessageServer, MessageClient, Message, Reply
from media_manager.application.widgets.window import Window
from media_manager.application.modules import ModulesKeeper, ModulesLoader


class ApplicationClient(MessageClient):
    def __init__(self, keeper: ModulesKeeper):
        super().__init__("Application", {
            "name": "Application"
        })
        self.__keeper = keeper

    def accepts(self, credits: dict[str, str]) -> bool:
        return self.__keeper.module_contains(credits.get("id", ""))

    def receive(self, message: Message) -> Reply:
        logging.info(message.content())
        return Reply(message.content())


class Application(QApplication):
    def __init__(self, app_location: Path):
        super().__init__()
        self.loader = ModulesLoader(app_location)
        self.window = Window()
        self.keeper = ModulesKeeper(self.window)

    def add_modules_location(self, location: Path):
        self.loader.add_modules_location(location)

    def load_modules(self):
        self.loader.find_all()
        for module in self.loader.load_all():
            self.keeper.module_add(module)

    def start(self) -> int:
        self.load_modules()
        self.window.show()
        return self.exec_()
