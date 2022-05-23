from pathlib import Path

from PySide2.QtWidgets import QApplication

from media_manager.application.widgets.window import Window
from media_manager.application.modules import Loader, Module


class Application(QApplication):
    def __init__(self, app_location: Path):
        super().__init__()
        self.loader = Loader(app_location)
        self.window = Window()

    def add_modules_location(self, location: Path):
        self.loader.add_modules_location(location)

    def start(self) -> int:
        self.loader.find_all()
        self.loader.load_all()
        self.window.modules_view.reload_widgets()
        self.window.show()
        return self.exec_()
