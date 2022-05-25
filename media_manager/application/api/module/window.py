from abc import ABC, abstractmethod

from PySide2.QtWidgets import QWidget


class ModuleWindow(ABC):
    @abstractmethod
    def window(self) -> QWidget:
        pass
