from abc import ABC, abstractmethod
from typing import Callable, Dict, List, Type
from .events import DomainEvent

EventHandler = Callable[[DomainEvent], None]

class EventBus(ABC):
    @abstractmethod
    async def publish(self, events: List[DomainEvent]) -> None:
        """Publish a list of domain events"""
        pass

    @abstractmethod
    def add_subscribers(self, subscribers: List[Type[DomainEvent]]) -> None:
        """Add subscribers for domain events"""
        pass

    @abstractmethod
    def subscribe(self, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        pass

    @abstractmethod
    def unsubscribe(self, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        pass

class InMemoryEventBus(EventBus):
    def __init__(self):
        self._handlers: Dict[Type[DomainEvent], List[EventHandler]] = {}

    async def publish(self, events: List[DomainEvent]) -> None:
        for event in events:
            event_type = type(event)
            if event_type in self._handlers:
                for handler in self._handlers[event_type]:
                    await handler(event)

    def subscribe(self, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def unsubscribe(self, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        if event_type in self._handlers:
            self._handlers[event_type].remove(handler)
            if not self._handlers[event_type]:
                del self._handlers[event_type]

    def add_subscribers(self, subscribers: List[Type[DomainEvent]]) -> None:
        # This method is not implemented in the InMemoryEventBus class
        # You may want to add the implementation here
        pass
