import json
import os
from datetime import datetime
from typing import Dict, Any, List
from ....domain.events import DomainEvent
from ..domain_event_json_serializer import DomainEventJsonSerializer

class DomainEventFailoverPublisher:
    def __init__(self, failover_path: str = "failed_domain_events"):
        self.failover_path = failover_path
        os.makedirs(failover_path, exist_ok=True)

    async def publish(self, domain_event: DomainEvent) -> None:
        event_json = DomainEventJsonSerializer.serialize(domain_event)
        file_name = f"{datetime.now().isoformat()}-{domain_event.event_id}.json"
        file_path = os.path.join(self.failover_path, file_name)
        
        with open(file_path, 'w') as f:
            json.dump(event_json, f)

    def consume_failed_events(self) -> List[Dict[str, Any]]:
        failed_events = []
        
        for file_name in os.listdir(self.failover_path):
            if file_name.endswith('.json'):
                file_path = os.path.join(self.failover_path, file_name)
                with open(file_path, 'r') as f:
                    event_json = json.load(f)
                    failed_events.append(event_json)
                os.remove(file_path)
        
        return failed_events
