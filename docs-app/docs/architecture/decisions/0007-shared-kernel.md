# 7. Shared Kernel para Bounded Contexts

Fecha: 2023-11-15

## Estado

Propuesto

## Contexto

Necesitamos un shared kernel que:
- Proporcione código común entre bounded contexts
- Defina contratos de integración
- Mantenga la consistencia del dominio
- Facilite la comunicación entre contextos

## Decisión

Implementaremos un shared kernel siguiendo la estructura actual del proyecto:

### 1. Estructura
```
src/
└── shared-kernel/           # Kernel compartido
    ├── domain/             # Lógica de dominio compartida
    │   ├── value-objects/  # Value Objects comunes
    │   │   ├── email.py
    │   │   ├── phone.py
    │   │   └── ulid.py
    │   └── events/        # Eventos de dominio
    │       ├── cv_analyzed.py
    │       └── process_updated.py
    └── infrastructure/    # Implementaciones técnicas
        ├── persistence/   # Componentes de persistencia
        │   ├── repository.py
        │   └── unit_of_work.py
        ├── messaging/     # Mensajería entre contextos
        │   ├── publisher.py
        │   └── subscriber.py
        └── services/      # Servicios compartidos
            ├── openai.py
            └── storage.py
```

### 2. Componentes Principales

#### Domain Layer
```python
# Value Objects
@dataclass(frozen=True)
class Email:
    value: str
    
    @classmethod
    def create(cls, value: str) -> 'Email':
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email format")
        return cls(value)

# Domain Events
class CVAnalyzed(DomainEvent):
    cv_id: ULID
    process_id: ULID
    score: float
    skills: List[str]
    summary: str
```

#### Infrastructure Layer
```python
# Repository Base
class Repository(Generic[T]):
    async def save(self, entity: T) -> T:
        raise NotImplementedError
    
    async def get_by_id(self, id: ULID) -> Optional[T]:
        raise NotImplementedError

# Event Publisher
class EventPublisher:
    async def publish(self, event: DomainEvent) -> None:
        raise NotImplementedError
```

### 3. Contratos de Integración
```python
# Interfaces
class CVAnalyzer(Protocol):
    async def analyze(self, cv: bytes) -> CVAnalysisResult:
        ...

class ProcessRepository(Protocol):
    async def get_active_processes(self) -> List[Process]:
        ...

# DTOs
@dataclass
class CVAnalysisResult:
    id: ULID
    score: float
    skills: List[str]
    experience: List[Experience]
    summary: str
```

## Implementación

### 1. Value Objects Compartidos
```python
@dataclass(frozen=True)
class ULID:
    value: str
    
    @classmethod
    def generate(cls) -> 'ULID':
        return cls(ulid.new().str)
    
    def __str__(self) -> str:
        return self.value
```

### 2. Eventos de Dominio
```python
class DomainEvent:
    id: ULID
    timestamp: datetime
    aggregate_id: ULID

    def to_dict(self) -> dict:
        return asdict(self)

class ProcessCreated(DomainEvent):
    title: str
    requirements: List[str]
    status: ProcessStatus
```

### 3. Servicios Compartidos
```python
class OpenAIService:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
    
    async def analyze_text(self, text: str) -> dict:
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": text}]
        )
        return response.choices[0].message.content
```

## Consecuencias

### Positivas
- Código reutilizable
- Contratos claros
- Consistencia entre contextos
- Mejor mantenibilidad

### Negativas
- Acoplamiento entre contextos
- Necesidad de coordinación
- Posible sobrecarga
- Gestión de dependencias

### Mitigaciones

1. **Acoplamiento**:
   - Interfaces claras
   - Dependencias mínimas
   - Versiones estables
   - Tests exhaustivos

2. **Coordinación**:
   - Documentación clara
   - Code reviews
   - Guías de contribución
   - Ownership definido

3. **Mantenimiento**:
   - CI/CD robusto
   - Versionado semántico
   - Breaking changes policy
   - Monitoreo de uso

## Referencias
- Clean Architecture
- Domain-Driven Design
- Event-Driven Architecture
- SOLID Principles
