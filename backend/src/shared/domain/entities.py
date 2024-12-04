from abc import ABC
from datetime import datetime
from typing import Any
from .value_objects import EntityId

class Entity(ABC):
    """Base class for all entities"""
    id: EntityId
    created_at: datetime
    updated_at: datetime

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Entity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
