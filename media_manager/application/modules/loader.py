import logging

from importlib import import_module
from pathlib import Path
from typing import Type

from media_manager.application.api import ModuleLoader
from media_manager.application.constants import APPLICATION_MODULE_API_VERSION

from .keeper import ModulesKeeper
from .module import Module


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
        self.modules_objects: dict[str, list[Module]] = {
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
                modules_objects = (module for module in map(import_module, modules_names))
                # Get public api class or default None singleton
                modules_loaders = (getattr(module, "PublicModuleLoader", object) for module in modules_objects)
                # Filter loaders by subclass check (all loaders must be subclass of ModuleLoader)
                modules_loaders = tuple(loader for loader in modules_loaders if issubclass(loader, ModuleLoader))
                self.modules_loaders.extend(modules_loaders)

    def load_all(self, keeper: ModulesKeeper):
        modules = [Module(loader()) for loader in self.modules_loaders]
        for module in sorted(modules, key=lambda mod: mod.loading_priority or 1):
            if module.module_meta is None:
                logging.error(f'{type(self).__name__}: Unable to load module without meta information')
                self.modules_objects["FAILURE"].append(module)
            elif not module.module_meta.is_supported_api(APPLICATION_MODULE_API_VERSION):
                logging.error(' '.join((
                    f'{type(self).__name__}:',
                    f'Unable to load module that is not support {APPLICATION_MODULE_API_VERSION} api version.',
                    f'Module id is `{module.id}`')))
                self.modules_objects["FAILURE"].append(module)
            else:
                self.modules_objects["SUCCESS"].append(module)
                keeper.module_add(module)

    def fetch_failure(self) -> list[Module]:
        return self.modules_objects["FAILURE"]

    def fetch_success(self) -> list[Module]:
        return self.modules_objects["SUCCESS"]
