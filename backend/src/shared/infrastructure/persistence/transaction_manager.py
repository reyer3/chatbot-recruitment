from typing import TypeVar, Callable, Awaitable, Optional, Any
from functools import wraps
import logging

from .unit_of_work import UnitOfWork, transaction_context
from ...domain.events import DomainEvent
from ..event_bus.in_memory_event_bus import InMemoryEventBus

T = TypeVar('T')
logger = logging.getLogger(__name__)


class TransactionManager:
    """Manages database transactions and domain events"""
    
    def __init__(
        self,
        uow: UnitOfWork,
        event_bus: Optional[InMemoryEventBus] = None
    ):
        self.uow = uow
        self.event_bus = event_bus or InMemoryEventBus()
        self._pending_events: list[DomainEvent] = []
    
    def add_event(self, event: DomainEvent) -> None:
        """Add a domain event to be published after transaction commit"""
        self._pending_events.append(event)
    
    async def _publish_events(self) -> None:
        """Publish all pending domain events"""
        try:
            for event in self._pending_events:
                await self.event_bus.publish(event)
        except Exception as e:
            logger.error(f"Error publishing events: {str(e)}")
            raise
        finally:
            self._pending_events.clear()
    
    def transactional(
        self,
        func: Callable[..., Awaitable[T]]
    ) -> Callable[..., Awaitable[T]]:
        """
        Decorator for handling transactions and domain events
        
        Usage:
            @transaction_manager.transactional
            async def create_process(self, command: CreateProcessCommand) -> None:
                # This code runs in a transaction
                process = Process.create(command)
                await self.repository.save(process)
        """
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            async with transaction_context(self.uow) as uow:
                try:
                    # Execute the function
                    result = await func(*args, **kwargs)
                    
                    # Publish events after successful commit
                    await self._publish_events()
                    
                    return result
                except Exception:
                    # Clear pending events on error
                    self._pending_events.clear()
                    raise
        
        return wrapper
