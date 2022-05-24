from abc import ABC

from .meta import ModuleMeta
from .widget import ModuleWidget
from .window import ModuleWindow


class ModuleLoader(ABC):
    def initialize_meta(self) -> ModuleMeta | None:
        return None

    def initialize_widget(self) -> ModuleWidget | None:
        return None

    def initialize_window(self) -> ModuleWindow | None:
        return None

    def loading_priority(self) -> float | None:
        return None
