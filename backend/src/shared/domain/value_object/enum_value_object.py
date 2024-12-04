from enum import Enum
from dataclasses import dataclass
from .value_object import ValueObject
from .invalid_argument_error import InvalidArgumentError

@dataclass(frozen=True)
class EnumValueObject(ValueObject):
    value: Enum

    def __post_init__(self):
        if not isinstance(self.value, Enum):
            raise InvalidArgumentError(f"<{self.__class__.__name__}> does not allow the value <{self.value}>")

    def __str__(self) -> str:
        return str(self.value.value)

    def equals(self, other: 'EnumValueObject') -> bool:
        return self.value == other.value
