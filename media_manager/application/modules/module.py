from media_manager.application.api import ModuleLoader, ModuleMeta, ModuleWidget


class NotLoaded:
    pass


class Module:
    def __init__(self, loader: ModuleLoader):
        self.__module_loader = loader
        self.__module_meta: ModuleMeta | None | NotLoaded = NotLoaded()
        self.__module_widget: ModuleWidget | None | NotLoaded = NotLoaded()

    @property
    def id(self):
        return self.module_meta.id()

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
