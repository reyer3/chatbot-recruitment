from datetime import datetime as dt
from typing import Any, Optional, Union

from ..errors import InvalidArgumentError
from .value_object import ValueObject


class DateTime(ValueObject):
    """Value object for handling dates and times"""
    
    def __init__(self, value: Union[str, dt, None] = None):
        """
        Initialize a DateTime value object
        Args:
            value: Can be:
                - None: Uses current UTC time
                - str: ISO format string
                - datetime: Python datetime object
        """
        if value is None:
            self._value = dt.utcnow()
        elif isinstance(value, str):
            try:
                self._value = dt.fromisoformat(value.replace('Z', '+00:00'))
            except ValueError as e:
                raise InvalidArgumentError(f"Invalid datetime format: {str(e)}")
        elif isinstance(value, dt):
            self._value = value
        else:
            raise InvalidArgumentError(f"Invalid datetime type: {type(value)}")
    
    @property
    def value(self) -> dt:
        return self._value
    
    def to_primitives(self) -> str:
        """Convert to ISO format string"""
        return self._value.isoformat()
    
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, DateTime):
            return False
        return self._value == other._value
    
    def __hash__(self) -> int:
        return hash(self._value)
    
    def __lt__(self, other: 'DateTime') -> bool:
        return self._value < other._value
    
    def __gt__(self, other: 'DateTime') -> bool:
        return self._value > other._value
    
    def __le__(self, other: 'DateTime') -> bool:
        return self._value <= other._value
    
    def __ge__(self, other: 'DateTime') -> bool:
        return self._value >= other._value
    
    @classmethod
    def now(cls) -> 'DateTime':
        """Create a DateTime with current UTC time"""
        return cls()
