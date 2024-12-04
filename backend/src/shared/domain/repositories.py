from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List
from .aggregate import AggregateRoot
from .value_objects import EntityId

T = TypeVar('T', bound=AggregateRoot)

class WriteRepository(Generic[T], ABC):
    """Interface for write operations"""
    
    @abstractmethod
    async def save(self, aggregate: T) -> None:
        """Save an aggregate"""
        pass

    @abstractmethod
    async def update(self, aggregate: T) -> None:
        """Update an aggregate"""
        pass

    @abstractmethod
    async def delete(self, aggregate_id: EntityId) -> None:
        """Delete an aggregate"""
        pass

class ReadRepository(Generic[T], ABC):
    """Interface for read operations"""
    
    @abstractmethod
    async def get_by_id(self, aggregate_id: EntityId) -> Optional[T]:
        """Get an aggregate by its ID"""
        pass

    @abstractmethod
    async def list_all(self) -> List[T]:
        """List all aggregates"""
        pass
