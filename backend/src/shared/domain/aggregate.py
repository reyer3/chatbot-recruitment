from typing import List
from .entities import Entity
from .events import DomainEvent
from .event_bus import EventBus

class AggregateRoot(Entity):
    def __init__(self):
        super().__init__()
        self._domain_events: List[DomainEvent] = []
        self._event_bus: EventBus = None

    def record_event(self, event: DomainEvent) -> None:
        """Record a domain event to be published later"""
        self._domain_events.append(event)

    def pull_domain_events(self) -> List[DomainEvent]:
        """Get and clear all recorded domain events"""
        events = self._domain_events[:]
        self._domain_events.clear()
        return events

    def set_event_bus(self, event_bus: EventBus) -> None:
        """Set the event bus for publishing events"""
        self._event_bus = event_bus

    async def publish_events(self) -> None:
        """Publish all recorded events through the event bus"""
        if self._event_bus:
            events = self.pull_domain_events()
            for event in events:
                await self._event_bus.publish(event)
