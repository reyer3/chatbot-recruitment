from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List
from ...domain.aggregate import AggregateRoot

T = TypeVar('T', bound=AggregateRoot)

class Repository(Generic[T], ABC):
    @abstractmethod
    async def save(self, aggregate: T) -> None:
        pass

    @abstractmethod
    async def search_by_id(self, id: str) -> Optional[T]:
        pass

    @abstractmethod
    async def search_all(self) -> List[T]:
        pass

    @abstractmethod
    async def delete(self, id: str) -> None:
        pass
