from dataclasses import dataclass
from typing import List, Dict, Any
from .filter import Filter

@dataclass(frozen=True)
class Filters:
    filters: List[Filter]

    @classmethod
    def from_values(cls, values: List[Dict[str, Any]]) -> 'Filters':
        return cls([
            Filter.from_values(
                str(item.get('field', '')),
                str(item.get('operator', '')),
                str(item.get('value', ''))
            )
            for item in values
        ])

    @classmethod
    def none(cls) -> 'Filters':
        return cls([])

    def has_filters(self) -> bool:
        return len(self.filters) > 0
