import threading

from media_manager.application.api.context import Context
from media_manager.application.api.module.components import CShutdown
from media_manager.application.api.module.features import FShutdown

from .storage import Storage


class CSettingsShutdown(CShutdown):
    def __init__(self, context: Context) -> None:
        super().__init__(context)
        self.__storage = context.unwrap("storage", Storage)

    def shutdown(self) -> None:
        self.__storage.save()
        # threading.Thread(target=self.__storage.save).run()
