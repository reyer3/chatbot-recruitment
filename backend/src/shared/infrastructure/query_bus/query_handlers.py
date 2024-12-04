from typing import Dict, Type, TypeVar, Generic
from ...domain.query import Query
from ...domain.response import Response
from ...domain.query_handler import QueryHandler

Q = TypeVar('Q', bound=Query)
R = TypeVar('R', bound=Response)

class QueryHandlers(Generic[Q, R]):
    def __init__(self):
        self._handlers: Dict[str, Type[QueryHandler]] = {}

    def register(self, query_class: Type[Q], handler: Type[QueryHandler[Q, R]]) -> None:
        self._handlers[query_class.__name__] = handler

    def get(self, query: Q) -> Type[QueryHandler[Q, R]]:
        handler = self._handlers.get(query.__class__.__name__)
        if not handler:
            raise ValueError(f'No handler registered for query {query.__class__.__name__}')
        return handler
