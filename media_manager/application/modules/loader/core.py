import inspect
import logging

from pathlib import Path
from typing import Generator, Type

from media_manager.application.api.context import Context
from media_manager.application.api.module import PrimitiveModule, ModuleLoader
from media_manager.application.constants import APPLICATION_API_VERSION

from .wrappers import Import, ImportLocations


class Loader:
    @staticmethod
    def __list_loaders_from(location: Path) -> list[Type[ModuleLoader]]:
        names = (path.parts[-1] for path in location.iterdir() if path.is_dir())
        modules = filter(None, (Import(name).make() for name in names))
        similar = (module.PublicModuleLoader for module in modules if hasattr(module, "PublicModuleLoader"))
        loaders = (loader for loader in similar if inspect.isclass(loader) and issubclass(loader, ModuleLoader))
        return list(loaders)

    @staticmethod
    def build_load_sequence(loaders: list[Type[ModuleLoader]]) -> list[Type[ModuleLoader]]:
        return sorted(loaders, key=lambda ld: ld.loading_priority() or 1)

    @staticmethod
    def find_from(*locations: Path) -> list[Type[ModuleLoader]]:
        with ImportLocations(*map(str, locations)):
            loaders: list[Type[ModuleLoader]] = []
            for location in locations:
                loaders.extend(Loader.__list_loaders_from(location))
            return loaders

    @staticmethod
    def load_from(*locations: Path, context: Context | None = None) -> Generator[PrimitiveModule, None, None]:
        loaders = Loader.find_from(*locations)
        loaders = Loader.build_load_sequence(loaders)
        for t_loader in loaders:
            try:
                o_loader = t_loader()
                if not o_loader.is_api_supported(APPLICATION_API_VERSION):
                    logging.warning(
                        "%s: Application module api version is not supported for module. Skipped...",
                        Loader.__name__)
                    continue
                yield o_loader.load().build(context=(context or Context()))
            except Exception as exc:  # pylint: disable=locally-disabled, broad-except
                logging.error("%s: Unable to load module. Skipped...",
                              Loader.__name__, exc_info=exc)
