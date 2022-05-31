import logging

from importlib import import_module
from types import ModuleType
from sys import path as sys_path


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
