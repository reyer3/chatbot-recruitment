# 3. Desarrollo Async-First

Fecha: 2023-11-15

## Estado

Aceptado

## Contexto

El sistema necesita manejar:
- Procesamiento de CVs en background
- Análisis de IA que pueden ser lentos
- Múltiples conexiones simultáneas
- Operaciones I/O intensivas

## Decisión

Adoptaremos un enfoque "async-first" utilizando:

1. **FastAPI y ASGI**:
   - Framework asíncrono nativo
   - Alto rendimiento
   - Soporte para WebSockets
   - Documentación automática

2. **SQLAlchemy 2.0**:
   - ORM asíncrono
   - Soporte para conexiones pooling
   - Transacciones asíncronas

3. **Celery para Tareas**:
   - Procesamiento en background
   - Escalabilidad horizontal
   - Monitoreo de tareas
   - Reintentos automáticos

## Implementación

### API Asíncrona
```python
@router.post("/processes")
async def create_process(
    request: CreateProcessRequest,
    use_case: CreateProcessUseCase = Depends()
) -> ProcessResponse:
    return await use_case.execute(request)
```

### Repositorio Asíncrono
```python
class AsyncProcessRepository:
    async def save(self, process: Process) -> Process:
        async with self.session() as session:
            await session.add(process)
            await session.commit()
            return process
```

### Tareas Background
```python
@celery_app.task(retry_policy={
    'max_retries': 3,
    'interval_start': 0,
    'interval_step': 0.2,
    'interval_max': 0.5,
})
async def analyze_cv(cv_id: str) -> dict:
    # Análisis asíncrono
    pass
```

## Consecuencias

### Positivas
- Mejor uso de recursos
- Mayor concurrencia
- Escalabilidad mejorada
- Responsividad de la API

### Negativas
- Complejidad adicional
- Debugging más difícil
- Necesidad de manejo de errores asíncrono
- Curva de aprendizaje para desarrolladores

## Referencias
- FastAPI Documentation
- SQLAlchemy 2.0 Documentation
- Celery Best Practices
