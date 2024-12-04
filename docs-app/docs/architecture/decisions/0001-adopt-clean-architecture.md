# 1. Adoptar Clean Architecture y DDD

Fecha: 2023-11-15

## Estado

Aceptado

## Contexto

Necesitamos una arquitectura que permita:
- Escalabilidad del sistema
- Mantenibilidad del código
- Testabilidad de componentes
- Independencia de frameworks
- Separación clara de responsabilidades

## Decisión

Adoptaremos Clean Architecture junto con principios de Domain-Driven Design (DDD) por:

### Clean Architecture
1. **Capas Independientes**:
   - Domain: Lógica de negocio y entidades
   - Application: Casos de uso
   - Infrastructure: Implementaciones técnicas
   - Interface: APIs y UI

2. **Principios**:
   - Dependency Rule: Las dependencias apuntan hacia adentro
   - Entities: Reglas de negocio centrales
   - Use Cases: Reglas de aplicación específicas
   - Interface Adapters: Conversión de datos
   - Frameworks & Drivers: Detalles técnicos

### Domain-Driven Design
1. **Bounded Contexts**:
   - Recruitment Processes
   - CV Analysis
   - Candidates
   - Shared Kernel

2. **Patrones Tácticos**:
   - Entidades y Value Objects
   - Agregados y Repositorios
   - Eventos de Dominio
   - Servicios de Dominio

## Implementación

### Estructura de Directorios
```
src/
├── apps/
│   └── api/
└── contexts/
    ├── shared/
    ├── recruitment_processes/
    ├── cv_analysis/
    └── candidates/
        ├── domain/
        ├── application/
        └── infrastructure/
```

### Ejemplo de Implementación
```python
# Domain
@dataclass
class Process:
    id: ULID
    title: str
    requirements: List[str]

# Application
class CreateProcessUseCase:
    def __init__(self, repository: ProcessRepository):
        self.repository = repository

    async def execute(self, data: dict) -> Process:
        process = Process.create(data)
        return await self.repository.save(process)

# Infrastructure
class PostgresProcessRepository(ProcessRepository):
    async def save(self, process: Process) -> Process:
        # Implementación específica
        pass
```

## Consecuencias

### Positivas
- Código altamente testeable
- Dominio rico y expresivo
- Cambios aislados por contexto
- Independencia de frameworks
- Mantenibilidad mejorada

### Negativas
- Mayor complejidad inicial
- Más código boilerplate
- Curva de aprendizaje
- Overhead en proyectos pequeños

## Referencias
- Clean Architecture (Robert C. Martin)
- Domain-Driven Design (Eric Evans)
- Hexagonal Architecture (Alistair Cockburn)
