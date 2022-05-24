from abc import ABC, abstractmethod
from pathlib import Path


class ModuleWidget(ABC):
    @abstractmethod
    def icon(self) -> Path:
        pass

    @abstractmethod
    def title(self) -> str:
        pass

    def alignment(self) -> str:
        return "BEGIN"
