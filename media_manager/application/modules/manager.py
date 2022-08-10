import logging

from media_manager.application.api.context import Context
from media_manager.application.api.module import PrimitiveModule, ModuleLoader
from media_manager.application.widgets.window import SupportableModule, Window

from media_manager.application.api.module.components.shutdown import CShutdown
from media_manager.application.api.module.features import FShutdown

from .loader import Resolver


class Manager:
    def __init__(self, context: Context) -> None:
        self.__context = context

        self.__resolver = Resolver()
        self.__window = Window()
        self.__modules: list[tuple[PrimitiveModule, ModuleLoader]] = []

    @property
    def window(self) -> Window:
        return self.__window

    @property
    def resolver(self) -> Resolver:
        return self.__resolver

    def load(self) -> None:
        for group in self.__resolver.resolve():
            for loader in group:
                self.__modules.append((loader.load().build(context=self.__context), loader))

        for module, _ in self.__modules:
            if isinstance(module, SupportableModule):
                self.__window.append(module)

        for pended in self.__resolver.pended():
            logging.error("Unable to load %s", pended.name())

    def unload(self) -> None:
        for attempts in range(1, 101):
            for index in reversed(range(len(self.__modules))):
                module, loader = self.__modules[index]

                if not self.__resolver.depended(loader):
                    del self.__modules[index]

                    shutdown = module.components().get(FShutdown, CShutdown)
                    if shutdown is not None:
                        shutdown.shutdown()

                    logging.debug("Module %s was unloaded", loader.name())
                else:
                    logging.warning("Unable to unload %s", loader.name())

            if not self.__modules:
                break

            logging.error("Attempts #%s: Not all modules were unload, retrying...", attempts)
