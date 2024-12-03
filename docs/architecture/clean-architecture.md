# Clean Architecture y Principios de Diseño

## Principios Arquitectónicos

### 1. Clean Architecture
- **Independencia de frameworks**: El dominio no depende de la existencia de ninguna biblioteca
- **Testeable**: La lógica de negocio puede probarse sin elementos externos
- **Independiente de la UI**: La interfaz puede cambiar sin cambiar el sistema
- **Independiente de la base de datos**: Se puede cambiar PostgreSQL por MongoDB
- **Independiente de cualquier elemento externo**: Las reglas de negocio no saben nada del mundo exterior

### 2. Vertical Slicing
Organización por características de negocio en lugar de capas técnicas:
- Cada contexto es independiente y autocontenido
- Facilita el desarrollo y mantenimiento por equipos
- Permite diferentes decisiones técnicas por contexto

### 3. Screaming Architecture
La estructura del código grita el propósito del sistema:
- Los nombres de directorios reflejan el dominio
- La estructura comunica la intención del negocio
- Fácil comprensión del propósito de cada componente

## Bounded Contexts

### 1. Recruitment Processes
**Responsabilidad**: Gestión de procesos de selección
- Crear y modificar procesos
- Definir requisitos y criterios
- Gestionar estados del proceso

```python
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from uuid import UUID

@dataclass(frozen=True)
class ProcessId:
    value: UUID

@dataclass(frozen=True)
class ProcessTitle:
    value: str

    def __post_init__(self):
        if len(self.value) < 3:
            raise ValueError("Title must be at least 3 characters long")

@dataclass(frozen=True)
class Requirement:
    description: str
    is_mandatory: bool

@dataclass
class RecruitmentProcess:
    id: ProcessId
    title: ProcessTitle
    requirements: List[Requirement]
    evaluation_criteria: "EvaluationCriteria"
    status: "ProcessStatus"
    created_at: datetime
    updated_at: Optional[datetime] = None

    def evaluate(self, candidate: "Candidate") -> "Evaluation":
        return self.evaluation_criteria.evaluate(candidate, self.requirements)
```

### 2. CV Analysis
**Responsabilidad**: Análisis y evaluación de CVs
- Procesar documentos
- Extraer información
- Evaluar según criterios

```python
from abc import ABC, abstractmethod
from typing import Protocol

class CVAnalyzer(Protocol):
    async def analyze(self, cv: "CV") -> "CVAnalysis":
        ...
    
    async def evaluate(
        self, 
        analysis: "CVAnalysis", 
        criteria: "EvaluationCriteria"
    ) -> "Evaluation":
        ...

class OpenAICVAnalyzer:
    def __init__(self, openai_client: "OpenAIClient"):
        self._openai = openai_client

    async def analyze(self, cv: "CV") -> "CVAnalysis":
        # Implementación con OpenAI
        ...
```

### 3. Candidates
**Responsabilidad**: Gestión de candidatos
- Almacenar información de candidatos
- Tracking de estado
- Gestión de evaluaciones

## Capa de Aplicación

### Casos de Uso
Cada operación del sistema se representa como un caso de uso:

```python
from dataclasses import dataclass
from typing import Protocol

class CVRepository(Protocol):
    async def find_by_id(self, cv_id: UUID) -> Optional["CV"]:
        ...
    async def save(self, cv: "CV") -> None:
        ...

@dataclass
class AnalyzeCVCommand:
    cv_id: UUID

class AnalyzeCVUseCase:
    def __init__(
        self,
        cv_analyzer: CVAnalyzer,
        cv_repository: CVRepository
    ):
        self._analyzer = cv_analyzer
        self._repository = cv_repository

    async def execute(self, command: AnalyzeCVCommand) -> None:
        cv = await self._repository.find_by_id(command.cv_id)
        if not cv:
            raise CVNotFoundError(command.cv_id)
            
        analysis = await self._analyzer.analyze(cv)
        cv.update_analysis(analysis)
        await self._repository.save(cv)
```

## Infraestructura

### 1. Persistencia
```python
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

class PostgresCVRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_id(self, cv_id: UUID) -> Optional[CV]:
        result = await self._session.execute(
            select(CVModel).where(CVModel.id == cv_id)
        )
        cv_model = result.scalar_one_or_none()
        return cv_model.to_domain() if cv_model else None

    async def save(self, cv: CV) -> None:
        cv_model = CVModel.from_domain(cv)
        self._session.add(cv_model)
        await self._session.commit()
```

### 2. Servicios Externos
```python
class OpenAIService:
    def __init__(self, api_key: str):
        self._client = AsyncOpenAI(api_key=api_key)

    async def analyze_cv(self, content: str) -> Dict[str, Any]:
        response = await self._client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Analiza el siguiente CV..."},
                {"role": "user", "content": content}
            ]
        )
        return response.choices[0].message.content
```

## Eventos de Dominio

```python
from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class DomainEvent:
    occurred_on: datetime = field(default_factory=datetime.utcnow)

@dataclass
class CVAnalyzedEvent(DomainEvent):
    cv_id: UUID
    analysis_result: "AnalysisResult"
```

## Testing

### 1. Unit Tests
```python
from unittest.mock import AsyncMock
import pytest

async def test_analyze_cv_use_case():
    # Arrange
    cv = CV(id=UUID("..."), content="...")
    mock_repo = AsyncMock(CVRepository)
    mock_repo.find_by_id.return_value = cv
    mock_analyzer = AsyncMock(CVAnalyzer)
    use_case = AnalyzeCVUseCase(mock_analyzer, mock_repo)
    
    # Act
    await use_case.execute(AnalyzeCVCommand(cv_id=cv.id))
    
    # Assert
    mock_analyzer.analyze.assert_called_once_with(cv)
    mock_repo.save.assert_called_once()
