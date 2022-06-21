from media_manager.application.api.module.loader import ModuleLoader
from media_manager.application.api.module.factory import ModuleFactory, ModuleBuilder

from media_manager.application.api.module.components import CMetaInformation
from media_manager.application.api.module.features import FMetaInformation

from .widget import CSettingsDefaultWidget, FDefaultWidget
from .window import CSettingsWindow, FWindow


class CSettingsMetaInformation(CMetaInformation):
    def id(self) -> str:
        return f"{self.name()} ({self.version()})"

    def name(self) -> str:
        return "Settings"

    def version(self) -> str:
        return "0.0.1"


class PublicModuleLoader(ModuleLoader):
    def is_api_supported(self, version: str) -> bool:
        # Checks major version (minor must provide back-compatibility)
        return version.split(".", 3)[0] == "0"

    def load(self) -> ModuleBuilder:
        return (ModuleFactory()
                .install_component(FMetaInformation, CSettingsMetaInformation)
                .install_component(FDefaultWidget, CSettingsDefaultWidget)
                .install_component(FWindow, CSettingsWindow)
                .assemble())

    @staticmethod
    def loading_priority() -> float | None:
        return 0.1
