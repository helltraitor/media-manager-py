from abc import ABC, abstractmethod
from typing import TypeVar
from weakref import ReferenceType, ref

from PySide2.QtWidgets import QWidget

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .module import Module
else:
    Module = TypeVar("Module")


class ModuleWindow(ABC):
    def __init__(self):
        self.__module: ReferenceType[Module] | None = None

    def link(self, module: Module):
        self.__module = ref(module)

    def module(self) -> Module | None:
        return self.__module()

    @abstractmethod
    def window(self) -> QWidget:
        pass
