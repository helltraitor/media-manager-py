from collections.abc import Sequence
from random import randint

from media_manager.application.api.context import Context
from media_manager.application.api.messages import Credits
from media_manager.application.api.module.loader import ModuleLoader
from media_manager.application.api.module.factory import ModuleFactory, ModuleBuilder

from media_manager.application.api.module.components import CMessageClient, CMetaInformation, CDefaultWidget
from media_manager.application.api.module.features import FMessages, FMetaInformation, FDefaultWidget

from media_manager.application.api.version import Version

from .window import CCloneWindow, FWindow

RANDOM_ID = str(randint(0, 10**6))

NAME = f"Clone"
VERSION = "0.0.1"
ID = f"{NAME} ({VERSION}) #{RANDOM_ID}"


class PublicModuleLoader(ModuleLoader):
    def dependencies(self) -> Sequence[tuple[str, Version]]:
        return [("Settings", Version(0))]

    def supports(self, version: Version) -> bool:
        return version.major == 0

    def name(self) -> str:
        return "Clone"

    def version(self) -> Version:
        return Version(0, 0, 1)

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
