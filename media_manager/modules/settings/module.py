import logging

from pathlib import Path

from media_manager.application.api.module.loader import ModuleLoader
from media_manager.application.api.module import Module
from media_manager.application.api.module.meta import ModuleMeta
from media_manager.application.api.module.widget import ModuleDefaultWidget
from media_manager.application.api.module.window import ModuleWindow

from .window import QWidget, Window


class ProtectedModuleMeta(ModuleMeta):
    def __init__(self):
        super().__init__()
        logging.info("Settings.ProtectedModuleMeta is successfully loaded")

    def id(self) -> str:
        return f"{self.name()} {self.version()}"

    def name(self) -> str:
        return "Settings"

    def version(self) -> str:
        return "0.0.1"


class ProtectedModuleWidget(ModuleDefaultWidget):
    def __init__(self):
        super().__init__()
        logging.info("Settings.ProtectedModuleWidget is successfully loaded")

    def icon(self) -> str:
        return str(Path(__file__).parent / "resources" / "carol-liao-adjust-icon.svg")

    def title(self) -> str:
        return "Settings"

    def type(self) -> str:
        return "System"


class ProtectedModuleWindow(ModuleWindow):
    def window(self) -> QWidget:
        return Window()


class PublicModuleLoader(ModuleLoader):
    def __init__(self):
        super().__init__()
        logging.info("Settings.ProtectedModuleLoader is successfully loaded")

    def is_api_supported(self, version: str) -> bool:
        # Checks major version (minor must provide back-compatibility)
        return version.split(".", 3)[0] == "0"

    def load(self) -> Module:
        return Module(ProtectedModuleMeta(), None, ProtectedModuleWidget(), ProtectedModuleWindow())

    def loading_priority(self) -> float | None:
        return 0.1
