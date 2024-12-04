from abc import ABC, abstractmethod
from typing import Type, TypeVar, Generic
from .query import Query
from .response import Response
from .query_handler import QueryHandler

Q = TypeVar('Q', bound=Query)
R = TypeVar('R', bound=Response)

class QueryBus(ABC, Generic[Q, R]):
    @abstractmethod
    async def ask(self, query: Q) -> R:
        """Execute a query and return its response"""
        pass

    @abstractmethod
    def register(self, query_class: Type[Q], handler: Type[QueryHandler[Q, R]]) -> None:
        """Register a handler for a specific query type"""
        pass
