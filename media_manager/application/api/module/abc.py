from media_manager.application.api.deferred import Deferred
from media_manager.application.api.module.components import (
    ComponentStorage,

    CDeferredChannel,
    CMessageClient,
    CMetaInformation,
    CWidget, CWindow
)
from media_manager.application.api.module.features import (
    FDeferred,
    FMessages,
    FMetaInformation,
    FWidget, FWindow
)


class Module:
    def __init__(self, components: ComponentStorage):
        self.__components = components

    def components(self) -> ComponentStorage:
        return self.__components


class PrimitiveModule(Module):
    def meta(self) -> CMetaInformation:
        return self.components().get_unwrap(FMetaInformation, CMetaInformation)


class DeferrableModule(Module):
    def defer(self, deferred: Deferred):
        self.components().get_unwrap(FDeferred, CDeferredChannel).defer(deferred)


class SociableModule(Module):
    def client(self) -> CMessageClient:
        return self.components().get_unwrap(FMessages, CMessageClient)


class ViewableModule(Module):
    def widget(self) -> CWidget:
        return self.components().get_unwrap(FWidget, CWidget)

    def window(self) -> CWindow:
        return self.components().get_unwrap(FWindow, CWindow)
