from random import randint

from media_manager.application.api.context import Context
from media_manager.application.api.module.loader import ModuleLoader
from media_manager.application.api.module.factory import ModuleFactory, ModuleBuilder

from media_manager.application.api.module.components import CMetaInformation
from media_manager.application.api.module.features import FMetaInformation

from .widget import CCloneDefaultWidget, FDefaultWidget
from .window import CCloneWindow, FWindow


class CCloneMetaInformation(CMetaInformation):
    def __init__(self, context: Context):
        super().__init__(context)
        self.__context = context

    def id(self) -> str:
        return f"{self.name()} ({self.version()})"

    def name(self) -> str:
        return f"Clone #{self.__context.unwrap('id', str)}"

    def version(self) -> str:
        return "0.0.1"


class PublicModuleLoader(ModuleLoader):
    def is_api_supported(self, version: str) -> bool:
        # Checks major version (minor must provide back-compatibility)
        return version.split(".", 3)[0] == "0"

    def load(self) -> ModuleBuilder:
        clone_context = Context().with_object(str(randint(0, 10**6)), name="id")

        return (ModuleFactory()
                .install_component(FMetaInformation, CCloneMetaInformation, context=clone_context)
                .install_component(FDefaultWidget, CCloneDefaultWidget, context=clone_context)
                .install_component(FWindow, CCloneWindow, context=clone_context)
                .assemble())
