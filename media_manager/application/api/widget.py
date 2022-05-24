from abc import ABC, abstractmethod


class ModuleWidget(ABC):
    def alignment(self) -> str:
        return "BEGIN"

    @abstractmethod
    def icon(self) -> str:
        pass

    @abstractmethod
    def title(self) -> str:
        pass
