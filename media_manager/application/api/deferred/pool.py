from dataclasses import dataclass, field
from queue import PriorityQueue
from weakref import ReferenceType

from .abc import Deferred


@dataclass(order=True)
class PrioritizedDeferred:
    priority: int
    item: Deferred = field(compare=False)


class DeferredPoolChannel:
    def __init__(self, pool: ReferenceType["DeferredPool"]):
        self.__pool = pool

    def defer(self, deferred: Deferred) -> bool:
        if pool := self.__pool():
            pool.defer(deferred)
        return pool is not None


class DeferredPool:
    def __init__(self):
        self.__queue: PriorityQueue[PrioritizedDeferred] = PriorityQueue()

    def channel(self) -> DeferredPoolChannel:
        return DeferredPoolChannel(ReferenceType(self))

    def defer(self, deferred: Deferred):
        self.__queue.put(PrioritizedDeferred(deferred.expected(), deferred))

    def process(self):
        if not self.__queue.empty():
            prioritized = self.__queue.get()
            if prioritized.item.pending():
                prioritized.item.execute()
                return
            self.__queue.put(prioritized)
