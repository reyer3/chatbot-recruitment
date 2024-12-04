# Guía de Contribución

## Proceso de Contribución

### 1. Preparación
- Fork del repositorio
- Clonar localmente
- Configurar remote upstream

### 2. Crear Branch
```bash
git checkout main
git pull upstream main
git checkout -b feature/nombre-feature
```

### 3. Desarrollo
- Seguir guías de estilo
- Escribir tests
- Documentar cambios

### 4. Commit
```bash
# Formato de mensaje
<tipo>(<alcance>): <descripción>

# Ejemplos
feat(candidates): add CV analysis endpoint
fix(whatsapp): correct message handling
docs(api): update OpenAPI specs
```

Tipos de commit:
- `feat`: Nueva característica
- `fix`: Corrección de bug
- `docs`: Documentación
- `style`: Formato
- `refactor`: Refactorización
- `test`: Tests
- `chore`: Mantenimiento

### 5. Pull Request
- Título descriptivo
- Descripción detallada
- Referencias a issues
- Screenshots si aplica

## Estándares de Código

### Python
```python
# Imports
from typing import Optional
import datetime

# Type hints
def process_candidate(
    candidate_id: str,
    score: Optional[float] = None
) -> bool:
    pass

# Docstrings
def analyze_cv(content: str) -> dict:
    """
    Analiza el contenido de un CV usando IA.

    Args:
        content: Contenido del CV en texto plano

    Returns:
        Dict con score y habilidades detectadas
    """
    pass
```

### TypeScript
```typescript
// Interfaces
interface Message {
  type: string;
  content: string;
  timestamp: Date;
}

// Type safety
function processMessage(message: Message): Promise<void> {
  // Implementation
}

// Error handling
async function sendMessage(to: string, content: string): Promise<void> {
  try {
    await whatsappClient.send(to, content);
  } catch (error) {
    logger.error('Failed to send message', { error, to });
    throw new MessageDeliveryError(error.message);
  }
}
```

## Revisión de Código

### Checklist
- [ ] Cumple con estándares de código
- [ ] Tests pasan localmente
- [ ] Documentación actualizada
- [ ] Sin código comentado
- [ ] Manejo de errores apropiado
- [ ] Logging adecuado
- [ ] Performance considerada
- [ ] Seguridad revisada

### Feedback
- Constructivo y específico
- Enfocado en el código
- Sugerir mejoras
- Reconocer buenos patrones

## CI/CD

### Checks Automáticos
- Linting
- Type checking
- Tests
- Cobertura
- Seguridad
- Build

### Deploy
- Review apps
- Staging automático
- Production manual

## Documentación

### Tipos
1. **Código**
   - Docstrings
   - Comentarios inline
   - Type hints

2. **API**
   - OpenAPI/Swagger
   - AsyncAPI
   - Postman collections

3. **Arquitectura**
   - ADRs
   - Diagramas
   - Guías técnicas

## Seguridad

### Prácticas
- No commits de secretos
- Validación de inputs
- Sanitización de outputs
- HTTPS siempre
- Autenticación/Autorización

### Reporte de Vulnerabilidades
- Proceso privado
- Template detallado
- Respuesta rápida
- Fix prioritario

## Soporte

### Canales
- GitHub Issues
- Slack
- Email

### Templates
- Bug report
- Feature request
- Question

## Licencia

Este proyecto está bajo la licencia MIT. Al contribuir:
- Aceptas licenciar tu código bajo MIT
- Confirmas autoría original
- Permites uso comercial
