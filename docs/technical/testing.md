# Estrategia de Testing

## Niveles de Testing

### 1. Unit Tests
- Pruebas aisladas de componentes
- Mock de dependencias
- Cobertura mínima: 80%

### 2. Integration Tests
- Pruebas de integración entre componentes
- Uso de containers para servicios externos
- Verificación de contratos

### 3. End-to-End Tests
- Pruebas de flujos completos
- Simulación de interacciones de usuario
- Verificación de integraciones externas

## Estructura de Tests

### Core Backend (Python)
```
tests/
├── unit/
│   ├── domain/
│   ├── application/
│   └── infrastructure/
├── integration/
│   ├── api/
│   ├── database/
│   └── events/
├── e2e/
│   └── flows/
└── conftest.py
```

### WhatsApp Service (TypeScript)
```
tests/
├── unit/
│   ├── handlers/
│   ├── services/
│   └── utils/
├── integration/
│   ├── api/
│   └── events/
└── e2e/
```

## Herramientas

### Python
- pytest
- pytest-asyncio
- pytest-cov
- pytest-mock
- factory-boy
- testcontainers

### TypeScript
- Jest
- Supertest
- ts-jest
- jest-mock-extended

## Ejemplos de Tests

### Unit Test (Python)
```python
@pytest.mark.asyncio
async def test_create_candidate():
    # Arrange
    candidate_data = CandidateFactory.build()
    repository = Mock(spec=CandidateRepository)
    service = CandidateService(repository)
    
    # Act
    result = await service.create(candidate_data)
    
    # Assert
    assert result.id is not None
    repository.save.assert_called_once()
```

### Integration Test (TypeScript)
```typescript
describe('WhatsApp Webhook', () => {
  it('should process incoming message', async () => {
    // Arrange
    const message = createMockMessage();
    
    // Act
    const response = await request(app)
      .post('/webhook')
      .send(message);
    
    // Assert
    expect(response.status).toBe(200);
    expect(messageQueue.hasMessage()).toBeTruthy();
  });
});
```

## Fixtures y Factories

### Python Fixtures
```python
@pytest.fixture
async def db():
    async with AsyncTestingSession() as session:
        yield session
        await session.rollback()

@pytest.fixture
def candidate_factory(db):
    return CandidateFactory(session=db)
```

### TypeScript Factories
```typescript
const createMockMessage = () => ({
  type: 'text',
  content: 'Hello',
  from: '+1234567890'
});
```

## Mocking

### Servicios Externos
```python
@pytest.fixture
def mock_openai():
    with patch('app.infrastructure.ai.OpenAIClient') as mock:
        yield mock

def test_analyze_cv(mock_openai):
    mock_openai.analyze.return_value = {
        'score': 0.8,
        'skills': ['Python', 'AI']
    }
    # Test implementation
```

### Eventos
```typescript
jest.mock('../events/publisher', () => ({
  publish: jest.fn()
}));
```

## Tests de API

### FastAPI
```python
@pytest.mark.asyncio
async def test_create_candidate_api(client):
    response = await client.post(
        '/candidates',
        json={'name': 'John Doe', 'email': 'john@example.com'}
    )
    assert response.status_code == 201
    assert response.json()['id'] is not None
```

### Express
```typescript
describe('POST /webhook', () => {
  it('validates signature', async () => {
    const response = await request(app)
      .post('/webhook')
      .set('X-Hub-Signature', invalidSignature)
      .send({});
    
    expect(response.status).toBe(401);
  });
});
```

## Cobertura de Código

### Python
```bash
# Ejecutar tests con cobertura
pytest --cov=app --cov-report=html

# Verificar umbral mínimo
pytest --cov=app --cov-fail-under=80
```

### TypeScript
```bash
# Ejecutar tests con cobertura
npm run test:coverage

# Configuración en package.json
{
  "jest": {
    "coverageThreshold": {
      "global": {
        "statements": 80,
        "branches": 80,
        "functions": 80,
        "lines": 80
      }
    }
  }
}
```

## CI/CD Integration

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
          
      - name: Run tests
        run: |
          pytest --cov=app --cov-report=xml
          
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

## Mejores Prácticas

1. **Naming**
   - Test names deben ser descriptivos
   - Seguir patrón: test_[función]_[escenario]_[resultado esperado]

2. **Organización**
   - Un archivo de test por módulo
   - Agrupar tests relacionados en clases
   - Mantener tests independientes

3. **Assertions**
   - Usar assertions específicos
   - Una aserción principal por test
   - Assertions auxiliares cuando necesario

4. **Datos de Prueba**
   - Usar factories para datos de prueba
   - Evitar datos hardcodeados
   - Mantener datos de prueba mínimos

5. **Mocking**
   - Mock solo lo necesario
   - Preferir fixtures sobre mocks inline
   - Verificar comportamiento, no implementación

6. **Mantenimiento**
   - Actualizar tests con cambios de código
   - Eliminar tests obsoletos
   - Refactorizar tests cuando necesario
