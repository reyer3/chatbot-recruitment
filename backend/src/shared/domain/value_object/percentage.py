from decimal import Decimal, ROUND_HALF_UP
from typing import Union, Any

from ..errors import InvalidArgumentError
from .value_object import ValueObject


class Percentage(ValueObject):
    """Value object for percentage values"""
    
    def __init__(self, value: Union[int, float, str, Decimal]):
        self._value = self._to_decimal(value)
        self._ensure_valid_percentage(self._value)
    
    @staticmethod
    def _to_decimal(value: Union[int, float, str, Decimal]) -> Decimal:
        try:
            if isinstance(value, str):
                # Remove % symbol if present
                value = value.strip(' %')
            return Decimal(str(value)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        except Exception as e:
            raise InvalidArgumentError(f"Could not convert {value} to Decimal: {str(e)}")
    
    @staticmethod
    def _ensure_valid_percentage(value: Decimal) -> None:
        if value < 0 or value > 100:
            raise InvalidArgumentError(f"Percentage must be between 0 and 100, got {value}")
    
    @property
    def value(self) -> Decimal:
        return self._value
    
    def to_primitives(self) -> float:
        """Convert to float for JSON serialization"""
        return float(self._value)
    
    def to_string(self, decimals: int = 2) -> str:
        """Format as percentage string with specified decimal places"""
        format_str = f"0.{'0' * decimals}%"
        return self._value.quantize(Decimal(f"0.{'0' * decimals}")).normalize().__format__(format_str)
    
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Percentage):
            return False
        return self._value == other._value
    
    def __hash__(self) -> int:
        return hash(self._value)
    
    def __lt__(self, other: 'Percentage') -> bool:
        return self._value < other._value
    
    def __gt__(self, other: 'Percentage') -> bool:
        return self._value > other._value
    
    def __le__(self, other: 'Percentage') -> bool:
        return self._value <= other._value
    
    def __ge__(self, other: 'Percentage') -> bool:
        return self._value >= other._value
