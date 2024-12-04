from abc import ABC, abstractmethod
from typing import List, Type
from .events import DomainEvent

class DomainEventSubscriber(ABC):
    @abstractmethod
    async def on(self, domain_event: DomainEvent) -> None:
        """Handle the domain event"""
        pass

    @classmethod
    @abstractmethod
    def subscribed_to(cls) -> List[Type[DomainEvent]]:
        """Return list of event types this subscriber handles"""
        pass
