# Módulo Shared

## Estructura General

```
backend/src/shared/
├── domain/
│   ├── aggregate.py              # Base para agregados
│   ├── command.py               # Base para comandos
│   ├── command_bus.py           # Interfaz de command bus
│   ├── command_handler.py       # Base para manejadores de comandos
│   ├── criteria/                # Sistema de filtrado y ordenamiento
│   │   ├── filter_operator.py
│   │   ├── filter.py
│   │   ├── filter_field.py
│   │   ├── filter_value.py
│   │   ├── order_type.py
│   │   ├── order_by.py
│   │   ├── order.py
│   │   ├── filters.py
│   │   └── criteria.py
│   ├── domain_event_subscriber.py # Base para suscriptores de eventos
│   ├── entities.py              # Base para entidades
│   ├── errors.py               # Sistema de errores de dominio
│   ├── event_bus.py            # Sistema de eventos de dominio
│   ├── events.py               # Base para eventos
│   ├── logger.py               # Interfaz de logging
│   ├── query.py                # Base para queries
│   ├── query_bus.py            # Interfaz de query bus
│   ├── query_handler.py        # Base para manejadores de queries
│   ├── repositories.py         # Base para repositorios
│   ├── response.py             # Base para respuestas
│   └── value_object/           # Value Objects
│       ├── value_object.py     # Base para value objects
│       ├── string_value_object.py
│       ├── int_value_object.py
│       ├── enum_value_object.py
│       ├── email.py
│       ├── datetime.py
│       ├── phone_number.py
│       ├── url.py
│       ├── percentage.py
│       └── ulid.py
└── infrastructure/
    ├── command_bus/
    │   ├── __init__.py
    │   └── in_memory_command_bus.py
    ├── event_bus/
    │   ├── __init__.py
    │   └── in_memory_event_bus.py
    ├── persistence/
    │   ├── redis/
    │   │   ├── redis_client.py
    │   │   └── cache_service.py
    │   ├── unit_of_work.py
    │   └── transaction_manager.py
    ├── query_bus/
    │   ├── __init__.py
    │   └── in_memory_query_bus.py
    └── logger.py

```

## Componentes Principales

### 1. Value Objects
Base para la creación de objetos inmutables que encapsulan reglas de negocio:

- **Básicos**:
  - `StringValueObject`: Para valores string
  - `IntValueObject`: Para valores numéricos
  - `EnumValueObject`: Para enumeraciones

- **Específicos**:
  - `Email`: Validación y normalización de emails
  - `DateTime`: Manejo de fechas y timestamps
  - `PhoneNumber`: Validación de números telefónicos
  - `URL`: Validación de URLs
  - `Percentage`: Manejo de porcentajes
  - `ULID`: Identificadores únicos ordenables

### 2. Sistema de Eventos
Implementación del patrón Event Sourcing:

- `EventBus`: Publicación y suscripción de eventos
- `DomainEvent`: Base para eventos de dominio
- `DomainEventSubscriber`: Base para suscriptores

### 3. Command y Query Buses (CQRS)
Separación de operaciones de lectura y escritura:

- `CommandBus`: Manejo de comandos (escritura)
- `QueryBus`: Manejo de queries (lectura)
- Implementaciones en memoria para desarrollo

### 4. Sistema de Criterios
Filtrado y ordenamiento flexible:

- `Criteria`: Composición de filtros y ordenamiento
- `Filter`: Condiciones de filtrado
- `Order`: Especificaciones de ordenamiento

### 5. Persistencia
Manejo de datos y transacciones:

- **Caché**:
  - `RedisClient`: Cliente base para Redis
  - `CacheService`: Servicio de caché de alto nivel

- **Transacciones**:
  - `UnitOfWork`: Patrón para transacciones atómicas
  - `TransactionManager`: Gestión de transacciones y eventos

## Uso del Módulo

### Value Objects
```python
from shared.domain.value_object import Email, DateTime

email = Email("user@example.com")
timestamp = DateTime.now()
```

### Eventos
```python
@event_bus.subscribe(UserCreated)
async def handle_user_created(event: UserCreated) -> None:
    await notification_service.notify_creation(event.user_id)
```

### Caché
```python
@cache_service.cached(expire=timedelta(minutes=30))
async def get_user_profile(user_id: str) -> dict:
    return await repository.get_profile(user_id)
```

### Transacciones
```python
@transaction_manager.transactional
async def create_process(command: CreateProcessCommand) -> None:
    process = Process.create(command)
    await repository.save(process)
    transaction_manager.add_event(ProcessCreated(process.id))
```

## Decisiones Arquitectónicas Relacionadas

1. [ADR-0001: Adoptar Clean Architecture](../architecture/decisions/0001-adopt-clean-architecture.md)
2. [ADR-0002: Usar ULID como Identificador](../architecture/decisions/0002-use-ulid-as-identifier.md)
3. [ADR-0008: Implementar CQRS Pattern](../architecture/decisions/0008-implement-cqrs-pattern-early.md)
4. [ADR-0009: Sistema de Caché y Transacciones](../architecture/decisions/0009-implement-cache-and-transactions.md)

## Próximos Pasos

1. **Testing**:
   - Implementar pruebas unitarias para todos los componentes
   - Agregar pruebas de integración para Redis y eventos

2. **Monitoreo**:
   - Agregar métricas para caché y transacciones
   - Implementar logging detallado

3. **Documentación**:
   - Agregar ejemplos para cada componente
   - Documentar patrones de uso comunes

4. **Optimizaciones**:
   - Evaluar uso de connection pooling
   - Implementar circuit breakers
   - Optimizar serialización/deserialización
