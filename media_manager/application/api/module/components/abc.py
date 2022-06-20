import logging

from typing import Optional, Type, TypeVar
from weakref import ReferenceType

from media_manager.application.api.context import Context
from media_manager.application.api.module.features import Feature

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from media_manager.application.api.module.abc import Module


class Component:
    def __init__(self, context: Context):
        self.__module: ReferenceType["Module"] | None = None

    def link(self, module: "Module"):
        self.__module = ReferenceType(module)

    def module(self) -> Optional["Module"]:
        if self.__module is not None:
            return self.__module()
        return None


class ComponentStorage:
    TComponent = TypeVar("TComponent", bound=Component)

    def __init__(self, components: dict[Feature, Component]):
        self.__components = components

    def load(self, components: dict[Feature, Component]):
        if self.__components:
            logging.error("%s: Attempting to load components while active. Components: %s",
                          type(self).__name__, repr(components))
            raise RuntimeError(f"Components cannot be loaded in active {type(self).__name__}")
        self.__components = components

    def get(self, feature: Feature, guard: Type[TComponent]) -> TComponent | None:
        candidate = self.__components.get(feature)
        if candidate is not None and isinstance(candidate, guard):
            return candidate
        return None

    def get_unwrap(self, feature: Feature, guard: Type[TComponent]) -> TComponent:
        candidate = self.__components.get(feature)
        if candidate is None:
            raise RuntimeError(f"Component with feature `{feature}` is not exists")
        if not isinstance(candidate, guard):
            raise RuntimeError(f"Component type `{type(candidate)}` is not instance of guard type `{guard}`")
        return candidate
