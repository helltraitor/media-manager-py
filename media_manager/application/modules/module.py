from media_manager.application.api import ModuleLoader, ModuleMeta, ModuleWidget, ModuleWindow


class NotLoaded:
    pass


class Module:
    def __init__(self, loader: ModuleLoader):
        self.__module_loader = loader
        self.__module_meta: ModuleMeta | None | NotLoaded = NotLoaded()
        self.__module_widget: ModuleWidget | None | NotLoaded = NotLoaded()
        self.__module_window: ModuleWindow | None | NotLoaded = NotLoaded()

    @property
    def id(self) -> str:
        return self.module_meta.id() if self.module_meta is not None else 'Module.id error'

    @property
    def loading_priority(self) -> float:
        return self.__module_loader.loading_priority() or 1

    @property
    def module_meta(self) -> ModuleMeta | None:
        if isinstance(self.__module_meta, NotLoaded):
            self.__module_meta = self.__module_loader.initialize_meta()
        return self.__module_meta

    @property
    def module_widget(self) -> ModuleWidget | None:
        if isinstance(self.__module_widget, NotLoaded):
            self.__module_widget = self.__module_loader.initialize_widget()
        return self.__module_widget

    @property
    def module_window(self) -> ModuleWindow | None:
        if isinstance(self.__module_window, NotLoaded):
            self.__module_window = self.__module_loader.initialize_window()
        return self.__module_window
