from abc import ABC, abstractmethod

from media_manager.application.api.module import Module


class ModuleLoader(ABC):
    @abstractmethod
    def is_api_supported(self, version: str) -> bool:
        pass

    @abstractmethod
    def load(self) -> Module:
        pass

    def loading_priority(self) -> float | None:
        return None
