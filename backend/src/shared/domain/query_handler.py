from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from .query import Query
from .response import Response

Q = TypeVar('Q', bound=Query)
R = TypeVar('R', bound=Response)

class QueryHandler(Generic[Q, R], ABC):
    @abstractmethod
    async def handle(self, query: Q) -> R:
        """Handle a query and return its response"""
        pass
