import logging

from pathlib import Path

from media_manager.application.api import ModuleLoader, ModuleMeta, ModuleWidget, ModuleWindow


class ProtectedModuleMeta(ModuleMeta):
    def __init__(self):
        logging.info("About.ProtectedModuleMeta is successfully loaded")

    def id(self) -> str:
        return f"{self.name()} {self.version()}"

    def is_supported_api(self, version: str) -> bool:
        # Checks major version (minor must provide back-compatibility)
        return version.split(".", 3)[0] == "0"

    def name(self) -> str:
        return "Settings"

    def version(self) -> str:
        return "0.0.1"


class ProtectedModuleWidget(ModuleWidget):
    def __init__(self):
        logging.info("About.ProtectedModuleWidget is successfully loaded")

    def alignment(self) -> str:
        return "END"

    def icon(self) -> str:
        return str(Path(__file__).parent / "resources" / "icon.svg")

    def title(self) -> str:
        return "About"


class PublicModuleLoader(ModuleLoader):
    def __init__(self):
        logging.info("About.ProtectedModuleLoader is successfully loaded")

    def initialize_meta(self) -> ModuleMeta | None:
        return ProtectedModuleMeta()

    def initialize_widget(self) -> ModuleWidget | None:
        return ProtectedModuleWidget()

    def loading_priority(self) -> float | None:
        return 0.05
