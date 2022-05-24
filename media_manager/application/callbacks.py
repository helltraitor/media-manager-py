from typing import Any, Callable, TypeAlias

from media_manager.application.filters import Filter, NoFilter


CallbackFunction: TypeAlias = Callable[[], Any]


class Callback:
    def __init__(self, *callbacks: CallbackFunction | "Callback"):
        self.__callbacks = callbacks
        self.__filter = NoFilter

    def call_on(self, obj: Any) -> bool:
        if not self.__filter.passed(obj):
            return False

        for callback in self.__callbacks:
            if isinstance(callback, Callback):
                callback.call_on(obj)
            else:
                callback()
        return True

    def with_filter(self, filter: Filter) -> "Callback":
        if self.__filter is not NoFilter:
            raise ValueError(
                f'{type(self).__name__}: `with_filter` method can be called only once, when NoFilter is using')
        self.__filter = filter
        return self
