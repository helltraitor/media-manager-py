from abc import ABC, abstractmethod


class ModuleMeta(ABC):
    @abstractmethod
    def id(self) -> str:
        pass

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def version(self) -> str:
        pass
