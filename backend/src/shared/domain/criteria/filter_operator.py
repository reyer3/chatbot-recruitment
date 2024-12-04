from enum import Enum, auto

class FilterOperator(Enum):
    EQUAL = '='
    NOT_EQUAL = '!='
    GT = '>'
    LT = '<'
    CONTAINS = 'CONTAINS'
    NOT_CONTAINS = 'NOT_CONTAINS'
    
    @classmethod
    def from_string(cls, value: str) -> 'FilterOperator':
        try:
            return cls(value)
        except ValueError:
            raise ValueError(f'Invalid filter operator {value}')
