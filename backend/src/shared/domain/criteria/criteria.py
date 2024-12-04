from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from .filters import Filters
from .order import Order

@dataclass(frozen=True)
class Criteria:
    filters: Filters
    order: Order
    offset: Optional[int] = None
    limit: Optional[int] = None

    @classmethod
    def from_values(
        cls,
        filters: List[Dict[str, Any]] = None,
        order_by: str = None,
        order_type: str = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None
    ) -> 'Criteria':
        return cls(
            filters=Filters.from_values(filters) if filters else Filters.none(),
            order=Order.from_values(order_by, order_type) if order_by and order_type else Order.none(),
            offset=offset,
            limit=limit
        )

    def has_filters(self) -> bool:
        return self.filters.has_filters()

    def has_order(self) -> bool:
        return self.order.has_order()
