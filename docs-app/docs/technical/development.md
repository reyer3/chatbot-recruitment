# Guía de Desarrollo

## Estructura del Proyecto

```
.
├── services/
│   ├── core/           # Backend principal (Python/FastAPI)
│   └── whatsapp/       # Servicio de WhatsApp (Node.js)
├── shared/             # Shared Kernel
│   ├── python/         # Implementación Python
│   └── typescript/     # Implementación TypeScript
└── docs/              # Documentación
```

## Estándares de Código

### Python (Core Backend)
- Python 3.11+ con type hints
- Black para formateo
- isort para imports
- Flake8 para linting
- pytest para testing
- mypy para type checking

### TypeScript (WhatsApp Service)
- Node.js 18+
- ESLint con Prettier
- Jest para testing
- TypeScript strict mode

## Flujo de Desarrollo

### 1. Crear Nueva Feature

```bash
# Crear rama feature
git checkout -b feature/nombre-feature

# Activar pre-commit hooks
pre-commit install
```

### 2. Desarrollo Local

#### Core Backend
```bash
cd services/core
uvicorn app.main:app --reload --port 8000
```

#### WhatsApp Service
```bash
cd services/whatsapp
npm run dev
```

### 3. Testing

```bash
# Core Backend
cd services/core
pytest
pytest --cov=app

# WhatsApp Service
cd services/whatsapp
npm test
npm run test:coverage
```

### 4. Code Review
- Crear Pull Request
- Asegurar cobertura de tests
- Pasar CI/CD checks
- Obtener aprobación

## Patrones y Mejores Prácticas

### Clean Architecture

```python
app/
├── domain/         # Entidades y reglas de negocio
├── application/    # Casos de uso
├── infrastructure/ # Implementaciones concretas
└── interfaces/     # Controllers y presentadores
```

### Domain-Driven Design
- Bounded Contexts claros
- Agregados bien definidos
- Value Objects inmutables
- Domain Events para comunicación

### Async First
```python
# Ejemplo de endpoint asíncrono
@router.post("/candidates")
async def create_candidate(
    candidate: CandidateCreate,
    service: CandidateService = Depends(get_candidate_service)
) -> CandidateResponse:
    return await service.create(candidate)
```

### Event-Driven
```python
# Publicar evento
await event_publisher.publish(
    "candidate.created",
    CandidateCreatedEvent(id=candidate.id)
)

# Consumir evento
@event_handler("candidate.created")
async def handle_candidate_created(event: CandidateCreatedEvent):
    await process_candidate(event.id)
```

## IDE Setup

### VSCode
Extensiones recomendadas:
- Python
- Pylance
- ESLint
- Prettier
- Thunder Client
- Docker

Settings:
```json
{
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

### PyCharm
- Habilitar type checking
- Configurar Black como formateador
- Activar formateo en guardado

## Debugging

### Core Backend
```python
# Usando debugger
import debugpy
debugpy.listen(("0.0.0.0", 5678))
debugpy.wait_for_client()
```

### WhatsApp Service
```typescript
// Usando debugger
debugger;
```

## Monitoreo y Logs

### Logging
```python
from app.core.logger import get_logger

logger = get_logger(__name__)
logger.info("Procesando candidato", extra={"candidate_id": id})
```

### Métricas
- Prometheus para métricas
- Grafana para visualización

## Documentación de API

### Core Backend
- OpenAPI (Swagger) en `/docs`
- ReDoc en `/redoc`

### WhatsApp Service
- OpenAPI para webhooks
- AsyncAPI para eventos

## Seguridad

### Autenticación
- JWT para APIs
- Refresh tokens
- Rate limiting

### Datos Sensibles
- No logs de datos personales
- Encriptación en tránsito
- Sanitización de inputs

## CI/CD

### GitHub Actions
- Tests automáticos
- Linting y type checking
- Build de imágenes
- Deploy a staging

### Ambientes
- Development (local)
- Staging
- Production

## Comandos Útiles

```bash
# Formatear código
make format

# Ejecutar tests
make test

# Construir imágenes
make build

# Iniciar servicios
make up

# Detener servicios
make down
```
