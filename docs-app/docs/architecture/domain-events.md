# Eventos de Dominio

## Contexto: CV Analysis

### CVUploaded
```python
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from typing import Optional

@dataclass(frozen=True)
class CVUploaded:
    cv_id: UUID
    file_name: str
    mime_type: str
    uploaded_at: datetime
    process_id: UUID
```

### CVAnalysisCompleted
```python
@dataclass(frozen=True)
class CandidateInfo:
    name: str
    email: str
    phone: str

@dataclass(frozen=True)
class Experience:
    company: str
    position: str
    start_date: datetime
    end_date: Optional[datetime]
    description: str

@dataclass(frozen=True)
class Education:
    degree: str
    institution: str
    graduation_year: int

@dataclass(frozen=True)
class CVAnalysisCompleted:
    cv_id: UUID
    analysis_id: UUID
    candidate_info: CandidateInfo
    extracted_data: dict[str, any]
    completed_at: datetime
```

### CVEvaluationCompleted
```python
from enum import Enum

class Recommendation(str, Enum):
    APPROVE = "APPROVE"
    REVIEW = "REVIEW"
    REJECT = "REJECT"

@dataclass(frozen=True)
class CVEvaluationCompleted:
    cv_id: UUID
    process_id: UUID
    evaluation_score: float
    main_reason: str
    positive_aspects: list[str]
    requirements_match: float
    recommendation: Recommendation
```

## Contexto: Recruitment Process

### ProcessCreated
```python
@dataclass(frozen=True)
class EvaluationCriteria:
    technical_skills: float
    experience: float
    education: float

@dataclass(frozen=True)
class ProcessCreated:
    process_id: UUID
    title: str
    requirements: list[str]
    evaluation_criteria: EvaluationCriteria
    created_at: datetime
```

### ProcessStatusChanged
```python
class ProcessStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"

@dataclass(frozen=True)
class ProcessStatusChanged:
    process_id: UUID
    old_status: ProcessStatus
    new_status: ProcessStatus
    changed_at: datetime
    reason: str
```

## Contexto: Candidates

### CandidateCreated
```python
@dataclass(frozen=True)
class CandidateCreated:
    candidate_id: UUID
    name: str
    email: str
    phone: str
    process_id: UUID
    cv_id: UUID
    created_at: datetime
```

### CandidateStatusUpdated
```python
class CandidateStatus(str, Enum):
    NEW = "NEW"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

@dataclass(frozen=True)
class CandidateStatusUpdated:
    candidate_id: UUID
    process_id: UUID
    old_status: CandidateStatus
    new_status: CandidateStatus
    updated_at: datetime
    reason: str
```

## Manejo de Eventos

### Event Bus
```python
from abc import ABC, abstractmethod
from typing import Callable, Type

class EventBus(ABC):
    @abstractmethod
    async def publish(self, event: any) -> None:
        pass

    @abstractmethod
    def subscribe(self, event_type: Type[any], handler: Callable) -> None:
        pass

class InMemoryEventBus(EventBus):
    def __init__(self):
        self._handlers: dict[Type[any], list[Callable]] = {}

    async def publish(self, event: any) -> None:
        event_type = type(event)
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                await handler(event)

    def subscribe(self, event_type: Type[any], handler: Callable) -> None:
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
```

### Ejemplo de Uso
```python
class CVAnalysisService:
    def __init__(self, event_bus: EventBus):
        self._event_bus = event_bus

    async def analyze_cv(self, cv: any) -> None:
        # Realizar análisis
        analysis_result = await self._perform_analysis(cv)
        
        # Publicar evento
        event = CVAnalysisCompleted(
            cv_id=cv.id,
            analysis_id=UUID(),
            candidate_info=analysis_result.candidate_info,
            extracted_data=analysis_result.data,
            completed_at=datetime.utcnow()
        )
        await self._event_bus.publish(event)

# Suscriptor
async def handle_cv_analysis_completed(event: CVAnalysisCompleted) -> None:
    # Iniciar evaluación
    pass

# Configuración
event_bus = InMemoryEventBus()
event_bus.subscribe(CVAnalysisCompleted, handle_cv_analysis_completed)
```

### Consideraciones
- Eventos inmutables (usando dataclasses frozen)
- Tipado estricto para mejor seguridad
- Manejo asíncrono de eventos
- Registro de eventos para auditoría
