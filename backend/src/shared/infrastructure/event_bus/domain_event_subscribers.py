from typing import Dict, List, Type
from ...domain.events import DomainEvent
from ...domain.domain_event_subscriber import DomainEventSubscriber

class DomainEventSubscribers:
    def __init__(self, subscribers: List[Type[DomainEventSubscriber]]):
        self.subscribers = subscribers

    def items(self) -> List[Type[DomainEventSubscriber]]:
        return self.subscribers

    def get_by_event(self, event_class: Type[DomainEvent]) -> List[Type[DomainEventSubscriber]]:
        return [
            subscriber for subscriber in self.subscribers
            if event_class.__name__ in [event.__name__ for event in subscriber.subscribed_to()]
        ]

    def register(self, subscriber: Type[DomainEventSubscriber]) -> None:
        self.subscribers.append(subscriber)
