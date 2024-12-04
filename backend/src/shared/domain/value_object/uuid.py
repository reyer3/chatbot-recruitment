from dataclasses import dataclass
from uuid import UUID, uuid4
from .string_value_object import StringValueObject
from .invalid_argument_error import InvalidArgumentError

@dataclass(frozen=True)
class Uuid(StringValueObject):
    def __post_init__(self):
        try:
            UUID(self.value)
        except ValueError:
            raise InvalidArgumentError(f"<{self.__class__.__name__}> does not allow the value <{self.value}>")

    @classmethod
    def random(cls) -> 'Uuid':
        return cls(str(uuid4()))
