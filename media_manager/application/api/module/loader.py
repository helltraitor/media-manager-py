from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from .factory import ModuleBuilder
from ..version import Version


@runtime_checkable
class ModuleLoader(Protocol):
    def dependencies(self) -> Sequence[tuple[str, Version]]:
        return ()

    def load(self) -> ModuleBuilder: ...

    def name(self) -> str: ...

    def supports(self, version: Version) -> bool: ...

    def version(self) -> Version: ...
