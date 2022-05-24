from typing import Any, Callable

from media_manager.application.filters import Filter, NoFilter


class Callback:
    def __init__(self, callback: Callable[[], None], filter: Filter = NoFilter):
        self.__callback = callback
        self.__filter = filter

    def call_on(self, obj: Any) -> bool:
        if self.__filter.passed(obj):
            self.__callback()
            return True
        return False
