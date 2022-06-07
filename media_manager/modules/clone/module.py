from random import randint

from media_manager.application.api.module.loader import ModuleLoader
from media_manager.application.api.module import Module
from media_manager.application.api.module.meta import ModuleMeta
from media_manager.application.api.module.widget import ModuleDefaultWidget
from media_manager.application.api.module.window import ModuleWindow

from .window import QWidget, Window

ID = randint(0, 10**6)


class ProtectedModuleMeta(ModuleMeta):
    def __init__(self):
        super().__init__()

    def id(self) -> str:
        return f"{self.name()} {self.version()}"

    def name(self) -> str:
        return str(ID)

    def version(self) -> str:
        return "0.0.1"


class ProtectedModuleWidget(ModuleDefaultWidget):
    def __init__(self):
        super().__init__()

    def title(self) -> str:
        return str(ID)


class ProtectedModuleWindow(ModuleWindow):
    def window(self) -> QWidget:
        return Window(str(ID))


class PublicModuleLoader(ModuleLoader):
    def __init__(self):
        super().__init__()

    def is_api_supported(self, version: str) -> bool:
        # Checks major version (minor must provide back-compatibility)
        return version.split(".", 3)[0] == "0"

    def load(self) -> Module:
        return Module(ProtectedModuleMeta(), ProtectedModuleWidget(), ProtectedModuleWindow())

    def loading_priority(self) -> float | None:
        return 1.0
