from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any
from uuid import uuid4

@dataclass
class DomainEvent(ABC):
    """Base class for domain events"""
    
    event_id: str
    occurred_on: datetime
    aggregate_id: str

    @classmethod
    def create(cls, aggregate_id: str, **kwargs) -> 'DomainEvent':
        return cls(
            event_id=str(uuid4()),
            occurred_on=datetime.utcnow(),
            aggregate_id=str(aggregate_id),
            **kwargs
        )

    def to_primitives(self) -> Dict[str, Any]:
        """Convert event to primitive types for serialization"""
        return {
            'event_id': self.event_id,
            'occurred_on': self.occurred_on.isoformat(),
            'aggregate_id': self.aggregate_id
        }
