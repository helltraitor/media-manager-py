from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from media_manager.application.api.module import ModuleWidget

from .core import ModuleEvent


class ModuleWidgetEvent(ModuleEvent):
    def __init__(self, module: "ModuleWidget"):
        self.__module = module

    @property
    def module(self) -> "ModuleWidget":
        return self.__module


class WidgetHoveredEvent(ModuleWidgetEvent):
    pass


class WidgetUnhoveredEvent(ModuleWidgetEvent):
    pass


class WidgetInstalledEvent(ModuleWidgetEvent):
    pass


class WidgetUninstalledEvent(ModuleWidgetEvent):
    pass


class WidgetFocusedEvent(ModuleWidgetEvent):
    pass


class WidgetUnfocusedEvent(ModuleWidgetEvent):
    pass
