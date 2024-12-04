from typing import Type, TypeVar, Generic
from ...domain.query import Query
from ...domain.response import Response
from ...domain.query_bus import QueryBus
from ...domain.query_handler import QueryHandler
from .query_handlers import QueryHandlers

Q = TypeVar('Q', bound=Query)
R = TypeVar('R', bound=Response)

class InMemoryQueryBus(QueryBus[Q, R], Generic[Q, R]):
    def __init__(self, query_handlers: QueryHandlers[Q, R]):
        self._query_handlers = query_handlers

    async def ask(self, query: Q) -> R:
        handler_class = self._query_handlers.get(query)
        handler = handler_class()
        return await handler.handle(query)

    def register(self, query_class: Type[Q], handler: Type[QueryHandler[Q, R]]) -> None:
        self._query_handlers.register(query_class, handler)
