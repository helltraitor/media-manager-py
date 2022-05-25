from .meta import ModuleMeta
from .widget import ModuleWidget
from .window import ModuleWindow


class Module:
    def __init__(self, meta: ModuleMeta, widget: ModuleWidget | None, window: ModuleWindow | None):
        self.__meta = meta
        self.__widget = widget
        self.__window = window

    @property
    def id(self) -> str:
        return self.meta.id()

    @property
    def meta(self) -> ModuleMeta:
        return self.__meta

    @property
    def widget(self) -> ModuleWidget | None:
        return self.__widget

    @property
    def window(self) -> ModuleWindow | None:
        return self.__window
