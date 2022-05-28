from typing import Type

from media_manager.application.api.events.abc import Event

from .listener import EventListener
from .subscription import EventSubscription


class EventPool:
    def __init__(self):
        self.__listeners: dict[Type[Event], set[EventListener]] = {}
        self.__subscriptions: set[EventSubscription] = set()

    def announce(self, event: Event):
        # Event is ABC, so it cannot be used, instead we should check if event have super classes
        for base in event.bases():
            for listener in self.__listeners.get(base, ()):
                listener.handle(event)

    def subscribe(self, listener: EventListener) -> EventSubscription | None:
        if not listener.events():
            return None

        for event in listener.events():
            self.__listeners.setdefault(event, set()).add(listener)

        subscription = EventSubscription(listener, self)
        self.__subscriptions.add(subscription)
        return subscription

    def unsubscribe(self, subscription: EventSubscription):
        if subscription in self.__subscriptions and subscription.cancelled():
            self.__subscriptions.remove(subscription)
            for event in subscription.listener.events():
                self.__listeners[event].remove(subscription.listener)
