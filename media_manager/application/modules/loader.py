import logging

from pathlib import Path
from types import ModuleType
from typing import Type

from media_manager.application.api.module.loader import ModuleLoader
from media_manager.application.constants import APPLICATION_MODULE_API_VERSION

from .keeper import ModulesKeeper


class Import:
    from importlib import import_module as unwrap

    def __init__(self, name: str, package: str | None = None):
        self.__module = None
        self.__name = name
        self.__package = package

    def make(self) -> ModuleType | None:
        if self.__module is None:
            # noinspection PyBroadException
            try:
                self.__module = Import.unwrap(self.__name, self.__package)
            except Exception:
                pass
        return self.__module


class ImportLocations:
    from sys import path as import_locations

    def __init__(self, *locations: str):
        self.import_locations = {
            location: location in ImportLocations.import_locations for location in locations
        }

    def __enter__(self):
        for location, appended in self.import_locations.items():
            if not appended:
                ImportLocations.import_locations.append(location)

    def __exit__(self, exc_type, exc_val, exc_tb):
        for location, appended in self.import_locations.items():
            if not appended:
                ImportLocations.import_locations.remove(location)


class ModulesLoader:
    def __init__(self, app_location: Path):
        self.app_location = app_location
        self.modules_locations: list[Path] = []
        self.modules_loaders: list[Type[ModuleLoader]] = []
        self.modules_objects: dict[str, list[ModuleLoader]] = {
            "SUCCESS": [],
            "FAILURE": []
        }

    def add_modules_location(self, location: Path):
        if not location.is_dir():
            logging.warning(f'{type(self).__name__}: Indicated location is not a directory: "{location}"')
            return
        self.modules_locations.append(location)

    def find_all(self):
        self.modules_loaders.clear()
        self.modules_objects["SUCCESS"].clear()
        self.modules_objects["FAILURE"].clear()

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

    def load_all(self, keeper: ModulesKeeper):
        loaders = [loader() for loader in self.modules_loaders]
        for loader in sorted(loaders, key=lambda lod: lod.loading_priority() or 1):
            if not loader.is_api_supported(APPLICATION_MODULE_API_VERSION):
                logging.error(' '.join((
                    f'{type(self).__name__}:',
                    f'Unable to load module that is not support {APPLICATION_MODULE_API_VERSION} api version.')))
                self.modules_objects["FAILURE"].append(loader)
            else:
                self.modules_objects["SUCCESS"].append(loader)
                keeper.module_add(loader.load())

    def fetch_failure(self) -> list[ModuleLoader]:
        return self.modules_objects["FAILURE"]

    def fetch_success(self) -> list[ModuleLoader]:
        return self.modules_objects["SUCCESS"]
