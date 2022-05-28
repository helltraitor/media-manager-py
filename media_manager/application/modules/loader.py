import logging

from importlib import import_module
from pathlib import Path
from types import ModuleType
from typing import Type
from sys import path as sys_path

from media_manager.application.api.module import Module, ModuleLoader
from media_manager.application.constants import APPLICATION_MODULE_API_VERSION

from .keeper import ModulesKeeper


class Import:
    def __init__(self, name: str, package: str | None = None):
        self.__module: ModuleType | None = None
        self.__name = name
        self.__package = package

    def make(self) -> ModuleType | None:
        if self.__module is None:
            try:
                self.__module = self.unwrap()
            except Exception as exc:
                logging.error(
                    f'{type(self).__name__}: Unable to import package with a module due to unexpected error',
                    exc_info=exc)
        return self.__module

    def unwrap(self) -> ModuleType:
        return import_module(self.__name, self.__package)


class ImportLocations:
    def __init__(self, *locations: str):
        self.system_locations: list[str] = sys_path
        self.import_locations: dict[str, bool] = {
            location: location in self.system_locations for location in locations
        }

    def __enter__(self):
        for location, appended in self.import_locations.items():
            if not appended:
                self.system_locations.append(location)

    def __exit__(self, exc_type, exc_val, exc_tb):
        for location, appended in self.import_locations.items():
            if not appended:
                self.system_locations.remove(location)


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
                continue

            module: Module | None = None
            try:
                module = loader.load()
            except Exception as exc:
                logging.error(f'{type(self).__name__}: Unable to load module due to unexpected error', exc_info=exc)
                self.modules_objects["FAILURE"].append(loader)

            if module is not None:
                self.modules_objects["SUCCESS"].append(loader)
                keeper.module_add(module)

    def fetch_failure(self) -> list[ModuleLoader]:
        return self.modules_objects["FAILURE"]

    def fetch_success(self) -> list[ModuleLoader]:
        return self.modules_objects["SUCCESS"]
