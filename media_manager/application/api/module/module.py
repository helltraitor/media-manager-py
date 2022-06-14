from .meta import ModuleMeta
from .widget import ModuleWidget
from .window import ModuleWindow


class Module:
    def __init__(self,
                 meta: ModuleMeta,
                 widget: ModuleWidget | None,
                 window: ModuleWindow | None):
        self.__meta = meta
        self.__widget = widget
        self.__window = window

        if widget is not None:
            widget.link(self)
        if window is not None:
            window.link(self)

    def id(self) -> str:
        return self.__meta.id()

    def meta(self) -> ModuleMeta:
        return self.__meta

    def widget(self) -> ModuleWidget | None:
        return self.__widget

    def window(self) -> ModuleWindow | None:
        return self.__window
