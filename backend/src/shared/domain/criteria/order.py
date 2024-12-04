from dataclasses import dataclass
from .order_by import OrderBy
from .order_type import OrderType

@dataclass(frozen=True)
class Order:
    order_by: OrderBy
    order_type: OrderType

    @classmethod
    def from_values(cls, order_by: str, order_type: str) -> 'Order':
        return cls(
            OrderBy(order_by),
            OrderType.from_string(order_type)
        )

    @classmethod
    def none(cls) -> 'Order':
        return cls(
            OrderBy(''),
            OrderType.NONE
        )

    def has_order(self) -> bool:
        return self.order_type != OrderType.NONE
