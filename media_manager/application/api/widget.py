from pathlib import Path

from abc import ABC, abstractmethod


class ModuleWidget(ABC):
    @abstractmethod
    def icon(self) -> Path:
        pass

    @abstractmethod
    def title(self) -> str:
        pass
