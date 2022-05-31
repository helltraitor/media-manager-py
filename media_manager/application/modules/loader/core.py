import logging

from pathlib import Path
from typing import Type, Generator

from media_manager.application.api.module import Module, ModuleLoader
from media_manager.application.constants import APPLICATION_MODULE_API_VERSION


from .wrappers import Import, ImportLocations


class ModulesLoader:
    def __init__(self, app_location: Path):
        self.app_location = app_location
        self.modules_locations: list[Path] = []
        self.modules_loaders: list[Type[ModuleLoader]] = []

    def add_modules_location(self, location: Path):
        if not location.is_dir():
            logging.warning(f'{type(self).__name__}: Indicated location is not a directory: "{location}"')
            return
        self.modules_locations.append(location)

    def find_all(self):
        self.modules_loaders.clear()

        with ImportLocations(str(self.app_location), *(str(location) for location in self.modules_locations)):
            for location in self.modules_locations:
                # Find all modules names in indicated import locations
                modules_names = (path.parts[-1] for path in location.iterdir() if path.is_dir())
                # Import these modules
                modules_objects = (module.make() for module in map(Import, modules_names))
                modules_objects = (module for module in modules_objects if module is not None)
                # Get public api class or default None singleton
                modules_loaders = (getattr(module, "PublicModuleLoader", object) for module in modules_objects)
                # Filter loaders by subclass check (all loaders must be subclass of ModuleLoader)
                modules_loaders = tuple(loader for loader in modules_loaders if issubclass(loader, ModuleLoader))
                self.modules_loaders.extend(modules_loaders)

    def load_all(self) -> Generator[Module, None, None]:
        loaders = [loader() for loader in self.modules_loaders]
        for loader in sorted(loaders, key=lambda lod: lod.loading_priority() or 1):
            if not loader.is_api_supported(APPLICATION_MODULE_API_VERSION):
                logging.error(' '.join((
                    f'{type(self).__name__}:',
                    f'Unable to load module that is not support {APPLICATION_MODULE_API_VERSION} api version.')))
                continue

            try:
                yield loader.load()
            except Exception as exc:
                logging.error(f'{type(self).__name__}: Unable to load module due to unexpected error', exc_info=exc)
