from media_manager.application.api.module.loader import ModuleLoader
from media_manager.application.api.module.factory import ModuleFactory, ModuleBuilder

from media_manager.application.api.module.components import CMetaInformation
from media_manager.application.api.module.features import FMetaInformation

from media_manager.application.api.version import Version


from .widget import CAboutDefaultWidget, FDefaultWidget
from .window import CAboutWindow, FWindow


class CAboutMetaInformation(CMetaInformation):
    def id(self) -> str:
        return f"{self.name()} ({self.version()})"

    def name(self) -> str:
        return "About"

    def version(self) -> str:
        return "0.0.1"


class PublicModuleLoader(ModuleLoader):
    def supports(self, version: Version) -> bool:
        return version.major == 0

    def name(self) -> str:
        return "About"

    def version(self) -> Version:
        return Version(0, 0, 1)

    def load(self) -> ModuleBuilder:
        return (ModuleFactory()
                .install_component(FMetaInformation, CAboutMetaInformation)
                .install_component(FDefaultWidget, CAboutDefaultWidget)
                .install_component(FWindow, CAboutWindow)
                .assemble())
