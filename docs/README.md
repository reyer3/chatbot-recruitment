# Sistema de Reclutamiento AI

## Estructura de Documentación

## Visión General

Sistema de reclutamiento potenciado por IA que integra:
- [Análisis automático de CVs](processes/cv-processing.md)
- [Chat por WhatsApp](integrations/whatsapp-integration.md)
- [Evaluación de candidatos](processes/recruitment.md)
- [Seguimiento de procesos](processes/recruitment.md)

## Arquitectura

### Componentes Principales
1. **Core Backend (Python/FastAPI)**
   - [Clean Architecture](architecture/clean-architecture.md)
   - [Domain-Driven Design](architecture/system-design.md)
   - [Async-first Development](architecture/decisions/0003-async-first-development.md)
   - [ULID como identificadores](architecture/decisions/0002-use-ulid-as-identifier.md)

2. **WhatsApp Service (Node.js)**
   - [BuilderBot framework](builder-bot/es/index.mdx)
   - [Microservicio independiente](architecture/system-design.md)
   - [Comunicación por mensajería](flows/conversation-flows.md)

3. **AI Stack**
   - [LangChain para orquestación](integrations/openai-integration.md)
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
