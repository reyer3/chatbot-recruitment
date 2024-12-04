from dataclasses import dataclass
from .value_object import ValueObject
from .invalid_argument_error import InvalidArgumentError

@dataclass(frozen=True)
class StringValueObject(ValueObject):
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise InvalidArgumentError(f"<{self.__class__.__name__}> does not allow the value <{self.value}>")

    def __str__(self) -> str:
        return self.value
