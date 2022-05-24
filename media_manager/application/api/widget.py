from abc import ABC, abstractmethod
from pathlib import Path


class ModuleWidget(ABC):
    def alignment(self) -> str:
        return "BEGIN"

    @abstractmethod
    def icon(self) -> Path:
        pass

    @abstractmethod
    def title(self) -> str:
        pass
