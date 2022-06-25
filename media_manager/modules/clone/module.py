from random import randint

from media_manager.application.api.context import Context
from media_manager.application.api.messages import Credits
from media_manager.application.api.module.loader import ModuleLoader
from media_manager.application.api.module.factory import ModuleFactory, ModuleBuilder

from media_manager.application.api.module.components import CMessageClient, CMetaInformation, CDefaultWidget
from media_manager.application.api.module.features import FMessages, FMetaInformation, FDefaultWidget

from .window import CCloneWindow, FWindow

RANDOM_ID = str(randint(0, 10**6))

NAME = f"Clone #{RANDOM_ID}"
VERSION = "0.0.1"
ID = f"{NAME} ({VERSION})"


class PublicModuleLoader(ModuleLoader):
    def is_api_supported(self, version: str) -> bool:
        # Checks major version (minor must provide back-compatibility)
        return version.split(".", 3)[0] == "0"

    def load(self) -> ModuleBuilder:
        custom = (Context()
                  .with_object(ID, name="id")
                  .with_object(NAME, name="title")
                  .with_object(NAME, name="name")
                  .with_object(VERSION, name="version")
                  .with_object(Credits(NAME, VERSION, ID), name="credits"))
        return (ModuleFactory()
                .install_component(FMetaInformation, CMetaInformation, context=custom)
                .install_component(FMessages, CMessageClient, context=custom)
                .install_component(FDefaultWidget, CDefaultWidget, context=custom)
                .install_component(FWindow, CCloneWindow, context=custom)
                .assemble())
