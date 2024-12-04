# Sistema de Caché y Transacciones

## Sistema de Caché

### Configuración
El sistema de caché utiliza Redis y requiere las siguientes variables de entorno:
```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=optional
```

### Uso del CacheService

#### 1. Decorator para Cacheo Automático
```python
from datetime import timedelta
from shared.infrastructure.persistence.redis import CacheService

cache_service = CacheService(redis_client, prefix="candidates")

@cache_service.cached(expire=timedelta(minutes=30))
async def get_candidate_profile(candidate_id: str) -> dict:
    return await repository.get_profile(candidate_id)
```

#### 2. Operaciones Manuales
```python
# Almacenar en caché
await cache_service.set(
    key="process:123",
    value=process_data,
    expire=timedelta(hours=1)
)

# Recuperar de caché
cached_data = await cache_service.get("process:123")

# Eliminar de caché
await cache_service.delete("process:123")
```

#### 3. Prefijos y Namespaces
```python
# Diferentes servicios para diferentes dominios
process_cache = CacheService(redis_client, prefix="processes")
candidate_cache = CacheService(redis_client, prefix="candidates")
analysis_cache = CacheService(redis_client, prefix="analysis")
```

## Sistema de Transacciones

### Unit of Work Pattern

#### 1. Configuración Básica
```python
from shared.infrastructure.persistence.unit_of_work import SqlAlchemyUnitOfWork
from shared.infrastructure.persistence.transaction_manager import TransactionManager

# Configuración
uow = SqlAlchemyUnitOfWork(session)
transaction_manager = TransactionManager(uow, event_bus)
```

#### 2. Uso con Decorator
```python
@transaction_manager.transactional
async def create_candidate(command: CreateCandidateCommand) -> None:
    # Crear candidato
    candidate = Candidate.create(command)
    await repository.save(candidate)
    
    # Agregar evento
    transaction_manager.add_event(
        CandidateCreated(
            candidate_id=candidate.id,
            process_id=command.process_id
        )
    )
```

#### 3. Uso con Contexto
```python
async def complex_operation():
    async with transaction_context(uow) as tx:
        # Múltiples operaciones
        await repository.save(entity1)
        await repository.save(entity2)
        
        # Si hay error, rollback automático
        if error_condition:
            raise DomainError("Operation failed")
```

### Eventos de Dominio

#### 1. Publicación de Eventos
```python
# Los eventos se publican automáticamente después del commit
@transaction_manager.transactional
async def update_process_status(command: UpdateProcessStatusCommand) -> None:
    process = await repository.get(command.process_id)
    process.update_status(command.new_status)
    
    transaction_manager.add_event(
        ProcessStatusUpdated(
            process_id=process.id,
            old_status=process.status,
            new_status=command.new_status
        )
    )
```

#### 2. Suscripción a Eventos
```python
@event_bus.subscribe(ProcessStatusUpdated)
async def handle_process_status_updated(event: ProcessStatusUpdated) -> None:
    # Notificar cambio de estado
    await notification_service.notify_status_change(
        process_id=event.process_id,
        new_status=event.new_status
    )
```

## Mejores Prácticas

### Caché
1. Usar TTL apropiados según el caso de uso
2. Implementar invalidación explícita cuando sea necesario
3. Usar prefijos consistentes por dominio
4. Monitorear el uso y hit ratio

### Transacciones
1. Mantener transacciones cortas
2. Usar eventos para efectos secundarios
3. Implementar retry policies para operaciones críticas
4. Logging detallado para debugging

## Monitoreo

### Métricas de Caché
- Hit ratio
- Memoria utilizada
- Claves más accedidas
- Tiempo de respuesta

### Métricas de Transacciones
- Tiempo de transacción
- Tasa de rollback
- Eventos publicados
- Errores por tipo
