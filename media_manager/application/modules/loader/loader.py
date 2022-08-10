import inspect
import logging

from pathlib import Path
from typing import Type

from media_manager.application.api.module import ModuleLoader
from media_manager.application.constants import APPLICATION_API_VERSION

from .resolver import Resolver
from .wrappers import Import, ImportLocations


class Loader:
    def __init__(self, locations: set[Path] | None = None) -> None:
        self.__locations: set[Path] = locations or set()

    def append(self, location: Path) -> None:
        self.__locations.add(location)

    def remove(self, location: Path) -> None:
        self.__locations.discard(location)

    def find(self) -> list[Type[ModuleLoader]]:
        loaders: list[Type[ModuleLoader]] = []
        with ImportLocations(self.__locations):
            for location in self.__locations:
                names = (path.parts[-1] for path in location.iterdir() if path.is_dir())
                modules = filter(None, (Import(name).make() for name in names))
                similar = (module.PublicModuleLoader for module in modules
                           if hasattr(module, "PublicModuleLoader"))
                loaders.extend(loader for loader in similar
                               if inspect.isclass(loader) and issubclass(loader, ModuleLoader))
        return loaders

    def load(self, resolver: Resolver) -> None:
        for loader in self.find():
            try:
                o_loader = loader()
                if not o_loader.supports(APPLICATION_API_VERSION):
                    logging.warning(
                        "%s: Application module api version is not supported for module. Skipped...",
                        Loader.__name__)
                    continue
            except Exception as exc:  # pylint: disable=locally-disabled, broad-except
                logging.error("%s: Unable to load module. Skipped...",
                              Loader.__name__, exc_info=exc)
            else:
                resolver.append(o_loader)
