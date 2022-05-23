from abc import ABC

from .meta import ModuleMeta
from .widget import ModuleWidget


class ModuleLoader(ABC):
    def initialize_meta(self) -> ModuleMeta | None:
        return None

    def initialize_widget(self) -> ModuleWidget | None:
        return None

    def loading_priority(self) -> float | None:
        return None
