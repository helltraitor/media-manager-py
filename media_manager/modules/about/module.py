import logging

from pathlib import Path

from media_manager.application.api.module.loader import ModuleLoader
from media_manager.application.api.module import Module
from media_manager.application.api.module.meta import ModuleMeta
from media_manager.application.api.module.widget import ModuleDefaultWidget


class ProtectedModuleMeta(ModuleMeta):
    def __init__(self):
        super().__init__()
        logging.info("About.ProtectedModuleMeta is successfully loaded")

    def id(self) -> str:
        return f"{self.name()} {self.version()}"

    def name(self) -> str:
        return "About"

    def version(self) -> str:
        return "0.0.1"


class ProtectedModuleWidget(ModuleDefaultWidget):
    def __init__(self):
        super().__init__()
        logging.info("About.ProtectedModuleWidget is successfully loaded")

    def icon(self) -> str:
        return str(Path(__file__).parent / "resources" / "carol-liao-inform-icon.svg")

    def title(self) -> str:
        return "About"


class PublicModuleLoader(ModuleLoader):
    def __init__(self):
        super().__init__()
        logging.info("About.ProtectedModuleLoader is successfully loaded")

    def is_api_supported(self, version: str) -> bool:
        # Checks major version (minor must provide back-compatibility)
        return version.split(".", 3)[0] == "0"

    def load(self) -> Module:
        return Module(ProtectedModuleMeta(), ProtectedModuleWidget(), None)

    def loading_priority(self) -> float | None:
        return 0.05
