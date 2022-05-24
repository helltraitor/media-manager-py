from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import Any, Callable, TypeAlias

FilterCallable: TypeAlias = Callable[[Any], bool]


class Filter:
    @abstractmethod
    def passed(self, obj: Any) -> bool:
        pass


class MultiFilter(Filter, ABC):
    def __init__(self, *filters: FilterCallable):
        self.__filters = list(filters)

    def __iter__(self) -> Iterator[FilterCallable]:
        return iter(self.__filters)

    def with_filter(self, filter: FilterCallable) -> "MultiFilter":
        self.__filters.append(filter)
        return self

    def with_filters(self, *filters: FilterCallable) -> "MultiFilter":
        self.__filters.extend(list(filters))
        return self


class SingleFilter(Filter):
    def __init__(self, filter: FilterCallable):
        self.__filter = filter

    def passed(self, obj: Any) -> bool:
        return self.__filter(obj)


class AnyFilter(MultiFilter):
    def passed(self, obj: Any) -> bool:
        return any(filter(obj) for filter in self)


class AllFilter(MultiFilter):
    def passed(self, obj: Any) -> bool:
        return all(filter(obj) for filter in self)


NoFilter = SingleFilter(lambda obj: True)
