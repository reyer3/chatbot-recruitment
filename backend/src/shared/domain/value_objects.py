from dataclasses import dataclass
from datetime import datetime
from typing import NewType
from ulid import ULID

EntityId = NewType('EntityId', ULID)

@dataclass(frozen=True)
class ValueObject:
    """Base class for value objects"""
    def equals(self, other: 'ValueObject') -> bool:
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

@dataclass(frozen=True)
class StringValueObject(ValueObject):
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise ValueError(f"{self.__class__.__name__} must be a string")
        if not self.value:
            raise ValueError(f"{self.__class__.__name__} cannot be empty")

@dataclass(frozen=True)
class DateTimeValueObject(ValueObject):
    value: datetime

    def __post_init__(self):
        if not isinstance(self.value, datetime):
            raise ValueError(f"{self.__class__.__name__} must be a datetime")
