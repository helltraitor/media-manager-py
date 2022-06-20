from abc import ABC, abstractmethod

from .factory import ModuleBuilder


class ModuleLoader(ABC):
    @abstractmethod
    def is_api_supported(self, version: str) -> bool:
        pass

    @abstractmethod
    def load(self) -> ModuleBuilder:
        pass

    @staticmethod
    def loading_priority() -> float | None:
        return None
