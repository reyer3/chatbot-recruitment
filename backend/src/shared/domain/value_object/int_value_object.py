from dataclasses import dataclass
from .value_object import ValueObject
from .invalid_argument_error import InvalidArgumentError

@dataclass(frozen=True)
class IntValueObject(ValueObject):
    value: int

    def __post_init__(self):
        if not isinstance(self.value, int):
            raise InvalidArgumentError(f"<{self.__class__.__name__}> does not allow the value <{self.value}>")

    def __str__(self) -> str:
        return str(self.value)

    def __int__(self) -> int:
        return self.value
