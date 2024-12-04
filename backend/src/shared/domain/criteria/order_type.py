from enum import Enum

class OrderType(Enum):
    ASC = 'asc'
    DESC = 'desc'
    NONE = 'none'

    @classmethod
    def from_string(cls, value: str) -> 'OrderType':
        try:
            return cls(value.lower())
        except ValueError:
            return cls.NONE
