# Sistema de Reclutamiento AI

## Estructura de Documentación

```
docs/
├── architecture/           # Decisiones y diseño arquitectónico
│   ├── decisions/         # ADRs numerados
│   └── diagrams/          # Diagramas de arquitectura
│
├── api/                   # Documentación de API
│   ├── endpoints.md       # Especificación de endpoints
│   └── schemas/          # Esquemas de datos
│
├── processes/            # Procesos de negocio
│   ├── cv-processing.md  # Procesamiento de CVs
│   └── recruitment.md    # Flujo de reclutamiento
│
├── integrations/         # Integraciones externas
│   ├── whatsapp/        # Integración WhatsApp
│   └── openai/          # Integración OpenAI
│
└── deployment/          # Configuración y despliegue
    ├── configuration.md # Variables de entorno
    └── kubernetes/      # Configuración K8s
```

## Visión General

Sistema de reclutamiento potenciado por IA que integra:
- Análisis automático de CVs
- Chat por WhatsApp
- Evaluación de candidatos
- Seguimiento de procesos

## Arquitectura

### Componentes Principales
1. **Core Backend (Python/FastAPI)**
   - Clean Architecture
   - Domain-Driven Design
   - Async-first
   - ULID como identificadores

2. **WhatsApp Service (Node.js)**
   - BuilderBot framework
   - Microservicio independiente
   - Comunicación por mensajería

3. **AI Stack**
   - LangChain para orquestación
   - Qdrant para búsqueda vectorial
   - LangGraph para flujos
   - LangSmith para monitoreo

### Integraciones
- WhatsApp Business API
- OpenAI GPT-4
- PostgreSQL
- RabbitMQ

## Estado Actual

### Completado
- Decisiones arquitectónicas base
- Diseño de API principal
- Estructura de dominios
- Estrategia de integración WhatsApp

### En Progreso
- Implementación de microservicios
- Procesamiento de CVs
- Flujos conversacionales
- Sistema de evaluación

### Pendiente
- Testing end-to-end
- Monitoreo y métricas
- Despliegue en producción
- Documentación de usuario

## Próximos Pasos

1. Completar documentación faltante:
   - Diagramas de arquitectura
   - Esquemas de API
   - Flujos de reclutamiento
   - Guías de despliegue

2. Crear backlog detallado:
   - Historias de usuario
   - Tareas técnicas
   - Estimaciones
   - Priorización

## Referencias

- [ADRs](./architecture/decisions/)
- [API Docs](./api/endpoints.md)
- [Deployment](./deployment/configuration.md)
- [Procesos](./processes/)
