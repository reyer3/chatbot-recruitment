from dataclasses import dataclass
from .filter_field import FilterField
from .filter_operator import FilterOperator
from .filter_value import FilterValue

@dataclass(frozen=True)
class Filter:
    field: FilterField
    operator: FilterOperator
    value: FilterValue

    @classmethod
    def from_values(cls, field: str, operator: str, value: str) -> 'Filter':
        return cls(
            FilterField(field),
            FilterOperator.from_string(operator),
            FilterValue(value)
        )
