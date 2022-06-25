from media_manager.application.api.module.loader import ModuleLoader
from media_manager.application.api.module.factory import ModuleFactory, ModuleBuilder

from media_manager.application.api.context import Context
from media_manager.application.api.messages import Credits

from media_manager.application.api.module.components import CMetaInformation
from media_manager.application.api.module.features import FMetaInformation

from .client import CSettingsMessageClient, FMessages
from .widget import CSettingsDefaultWidget, FDefaultWidget
from .window import CSettingsWindow, FWindow


NAME = "Settings"
VERSION = "0.0.1"
ID = f"{NAME} ({VERSION})"


class CSettingsMetaInformation(CMetaInformation):
    def id(self) -> str:
        return ID

    def name(self) -> str:
        return NAME

    def version(self) -> str:
        return VERSION


class PublicModuleLoader(ModuleLoader):
    def is_api_supported(self, version: str) -> bool:
        # Checks major version (minor must provide back-compatibility)
        return version.split(".", 3)[0] == "0"

    def load(self) -> ModuleBuilder:
        return (ModuleFactory()
                .install_component(FMetaInformation, CSettingsMetaInformation)
                .install_component(FMessages, CSettingsMessageClient,
                                   context=Context().with_object(Credits(NAME, VERSION, ID), name="credits"))
                .install_component(FDefaultWidget, CSettingsDefaultWidget)
                .install_component(FWindow, CSettingsWindow)
                .assemble())

    @staticmethod
    def loading_priority() -> float | None:
        return 0.1
