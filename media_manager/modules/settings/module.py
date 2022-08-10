import threading

from media_manager.application.api.module.loader import ModuleLoader
from media_manager.application.api.module.factory import ModuleFactory, ModuleBuilder

from media_manager.application.api.context import Context
from media_manager.application.api.messages import Credits

from media_manager.application.api.module.components import CMetaInformation
from media_manager.application.api.module.features import FMetaInformation

from media_manager.application.api.version import Version

from .client import CSettingsMessageClient, FMessages
from .widget import CSettingsDefaultWidget, FDefaultWidget
from .window import CSettingsWindow, FWindow
from .shutdown import CSettingsShutdown, FShutdown
from .storage import Storage


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
    def supports(self, version: Version) -> bool:
        return version.major == 0

    def name(self) -> str:
        return "Settings"

    def version(self) -> Version:
        return Version(0, 0, 1)

    def load(self) -> ModuleBuilder:
        storage = Storage()
        threading.Thread(target=storage.load).start()

        return (ModuleFactory()
                .install_component(FMetaInformation, CSettingsMetaInformation)
                .install_component(FMessages, CSettingsMessageClient,
                                   context=(Context()
                                            .with_object(Credits(NAME, VERSION, ID), name="credits")
                                            .with_object(storage, name="storage")))
                .install_component(FShutdown, CSettingsShutdown,
                                   context=(Context()
                                            .with_object(storage, name="storage")))
                .install_component(FDefaultWidget, CSettingsDefaultWidget)
                .install_component(FWindow, CSettingsWindow)
                .assemble())

    @staticmethod
    def loading_priority() -> float | None:
        return 0.1
