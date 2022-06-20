from media_manager.application.api.context import Context
from media_manager.application.api.deferred import Deferred, DeferredPoolChannel

from .abc import Component


class CDeferredChannel(Component):
    def __init__(self, context: Context):
        super().__init__(context)
        self.__channel = context.unwrap(DeferredPoolChannel.__name__, DeferredPoolChannel)

    def defer(self, deferred: Deferred):
        self.__channel.defer(deferred)
