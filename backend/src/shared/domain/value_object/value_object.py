from abc import ABC
from typing import Any
from dataclasses import dataclass

@dataclass(frozen=True)
class ValueObject(ABC):
    """Base class for all value objects.
    En Python usamos frozen=True para hacer los value objects inmutables,
    similar al comportamiento en TypeScript."""
    
    def equals(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__
