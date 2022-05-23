from abc import ABC, abstractmethod


class ModuleMeta(ABC):
    @abstractmethod
    def id(self) -> str:
        pass

    @abstractmethod
    def is_supported_api(self, version: str) -> bool:
        pass

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def version(self) -> str:
        pass
