from dataclasses import dataclass
from ulid import ULID as ULIDLib
from .string_value_object import StringValueObject
from .invalid_argument_error import InvalidArgumentError

@dataclass(frozen=True)
class Ulid(StringValueObject):
    def __post_init__(self):
        try:
            ULIDLib.from_str(self.value)
        except ValueError:
            raise InvalidArgumentError(f"<{self.__class__.__name__}> does not allow the value <{self.value}>")

    @classmethod
    def random(cls) -> 'Ulid':
        """Generate a new random ULID"""
        return cls(str(ULIDLib()))
