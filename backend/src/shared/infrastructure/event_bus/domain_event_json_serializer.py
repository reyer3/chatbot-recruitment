from typing import Dict, Any
from datetime import datetime
from ...domain.events import DomainEvent

class DomainEventJsonSerializer:
    @staticmethod
    def serialize(domain_event: DomainEvent) -> Dict[str, Any]:
        return {
            'data': {
                'id': str(domain_event.event_id),
                'type': domain_event.__class__.__name__,
                'occurred_on': domain_event.occurred_on.isoformat(),
                'attributes': domain_event.to_primitives()
            },
            'meta': {
                'version': '1.0'
            }
        }

    @staticmethod
    def deserialize(event_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'id': event_data['data']['id'],
            'type': event_data['data']['type'],
            'occurred_on': datetime.fromisoformat(event_data['data']['occurred_on']),
            'attributes': event_data['data']['attributes']
        }
