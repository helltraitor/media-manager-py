from typing import Protocol, runtime_checkable

from media_manager.application.api.module.components import CMetaInformation, CWidget, CWindow


@runtime_checkable
class SupportableModule(Protocol):
    def meta(self) -> CMetaInformation: ...

    def widget(self) -> CWidget: ...

    def window(self) -> CWindow: ...
