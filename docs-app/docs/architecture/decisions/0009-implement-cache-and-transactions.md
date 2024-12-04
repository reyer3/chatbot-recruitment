# 9. Implementar Sistema de Caché y Transacciones

Fecha: 2024-01-24

## Estado

Aceptado

## Contexto

El sistema necesita manejar:
- Operaciones costosas y repetitivas (análisis de CV con IA)
- Sesiones de usuario (WhatsApp)
- Transacciones complejas con eventos de dominio
- Consistencia en operaciones distribuidas

## Decisión

Implementaremos dos sistemas fundamentales:

### 1. Sistema de Caché con Redis

#### Componentes
1. **RedisClient**:
   - Wrapper sobre redis-py
   - Operaciones CRUD asíncronas
   - Serialización/deserialización automática
   - Manejo de conexiones pooling

2. **CacheService**:
   - Generación de claves consistente
   - Prefijos por dominio
   - Expiración configurable
   - Decorator para cacheo automático

#### Usos Principales
- Resultados de análisis de CV
- Sesiones de WhatsApp
- Resultados de queries frecuentes
- Estados intermedios de procesos

### 2. Sistema de Transacciones

#### Componentes
1. **UnitOfWork**:
   - Patrón Unit of Work
   - Manejo de transacciones atómicas
   - Rollback automático en errores
   - Contexto asíncrono

2. **TransactionManager**:
   - Coordinación de transacciones
   - Publicación de eventos post-commit
   - Decorator transactional
   - Manejo de errores integrado

#### Usos Principales
- Creación/actualización de procesos
- Evaluación de candidatos
- Análisis de CV
- Operaciones que requieren eventos

## Implementación

### Caché
```python
@cache_service.cached(expire=timedelta(minutes=30))
async def get_candidate_analysis(cv_id: str) -> dict:
    # El resultado se cachea automáticamente
    return await analyzer.analyze(cv_id)

# Uso directo
await cache_service.set("key", value, expire=timedelta(hours=1))
cached_value = await cache_service.get("key")
```

### Transacciones
```python
@transaction_manager.transactional
async def create_process(command: CreateProcessCommand) -> None:
    # Todo esto se ejecuta en una transacción
    process = Process.create(command)
    await repository.save(process)
    
    # El evento se publica después del commit
    transaction_manager.add_event(ProcessCreated(process.id))

# Uso con contexto
async with transaction_context(uow) as tx:
    await repository.save(entity)
    # Commit automático al salir del contexto
```

## Consecuencias

### Positivas
- Mejor rendimiento con caché
- Consistencia garantizada en transacciones
- Manejo robusto de errores
- Código más limpio con decorators
- Separación clara de responsabilidades
- Publicación confiable de eventos

### Negativas
- Complejidad adicional en la infraestructura
- Necesidad de gestionar Redis
- Posibles problemas de consistencia de caché
- Overhead en transacciones simples

### Mitigaciones
1. **Complejidad**:
   - Abstracciones claras
   - Documentación detallada
   - Patrones consistentes

2. **Caché**:
   - TTL por defecto
   - Invalidación explícita
   - Monitoreo de uso

3. **Transacciones**:
   - Timeouts configurables
   - Retry policies
   - Logging detallado

## Referencias
- Redis Documentation
- SQLAlchemy Transaction Guide
- Domain Events Best Practices
- Clean Architecture Guidelines
