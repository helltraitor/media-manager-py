from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from media_manager.application.api.module import ViewableModule

from .core import ModuleEvent


class ModuleWidgetEvent(ModuleEvent):
    def __init__(self, module: "ViewableModule"):
        self.__module = module

    def module(self) -> "ViewableModule":
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
