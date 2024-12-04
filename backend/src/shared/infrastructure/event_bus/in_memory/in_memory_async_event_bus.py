from typing import List, Type
from ....domain.events import DomainEvent
from ....domain.event_bus import EventBus
from ..domain_event_subscribers import DomainEventSubscribers
from ..domain_event_failover_publisher.domain_event_failover_publisher import DomainEventFailoverPublisher

class InMemoryAsyncEventBus(EventBus):
    def __init__(
        self,
        subscribers: DomainEventSubscribers,
        failover_publisher: DomainEventFailoverPublisher
    ):
        self.subscribers = subscribers
        self.failover_publisher = failover_publisher

    async def publish(self, events: List[DomainEvent]) -> None:
        for event in events:
            subscribers = self.subscribers.get_by_event(type(event))
            
            try:
                for subscriber in subscribers:
                    subscriber_instance = subscriber()
                    await subscriber_instance.on(event)
            except Exception as e:
                # Si falla la publicación, guardamos el evento para retry
                await self.failover_publisher.publish(event)
                raise e

    def add_subscribers(self, subscribers: List[Type[DomainEvent]]) -> None:
        for subscriber in subscribers:
            self.subscribers.register(subscriber)
