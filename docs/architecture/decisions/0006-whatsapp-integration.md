# 6. Integración con WhatsApp usando BuilderBot

Fecha: 2023-11-15

## Estado

Propuesto

## Contexto

Necesitamos:
- Canal de comunicación directo con candidatos
- Interfaz conversacional accesible
- Procesamiento automático de respuestas
- Integración con nuestro sistema de IA
- **Integración con backend Python existente**

## Decisión

Implementaremos BuilderBot como un microservicio independiente:

### 1. Arquitectura de Microservicios
```
┌─────────────────┐      ┌──────────────────┐
│  WhatsApp Bot   │      │  Core Backend    │
│   (Node.js)     │◄────►│    (Python)      │
│   BuilderBot    │      │   FastAPI        │
└─────────────────┘      └──────────────────┘
         ▲                        ▲
         │                        │
         ▼                        ▼
┌─────────────────┐      ┌──────────────────┐
│    Message      │      │   Recruitment    │
│     Queue       │      │    Database      │
│   (RabbitMQ)    │      │   (PostgreSQL)   │
└─────────────────┘      └──────────────────┘
```

### 2. Componentes del Sistema
- **WhatsApp Service** (Node.js/BuilderBot):
  * Manejo de conexión WhatsApp
  * Flujos conversacionales básicos
  * Queue de mensajes
  * Forwarding a backend Python

- **Core Backend** (Python/FastAPI):
  * Lógica de negocio principal
  * Procesamiento de CV
  * Análisis de IA
  * Gestión de candidatos

### 3. Comunicación entre Servicios
```typescript
// WhatsApp Service (BuilderBot)
const cvFlow = addKeyword(['cv', 'aplicar'])
    .addAnswer('Por favor, envía tu CV en PDF.')
    .addAction(async (ctx, { flowDynamic }) => {
        // Enviar a cola de mensajes
        await messageQueue.publish('cv.received', {
            whatsappId: ctx.from,
            attachment: ctx.message.attachment,
            timestamp: Date.now()
        })
        
        await flowDynamic('Gracias, procesaremos tu CV.')
    })

// Escuchar respuestas del backend
messageQueue.subscribe('cv.processed', async (data) => {
    const { whatsappId, result } = data
    await bot.sendMessage(whatsappId, result.summary)
})
```

```python
# Core Backend (Python/FastAPI)
class CVProcessor:
    def __init__(self, message_queue: MessageQueue):
        self.queue = message_queue
        
    async def process_cv(self, message: dict):
        # Procesar CV con nuestro stack de IA
        cv_data = await self.analyze_cv(message['attachment'])
        
        # Enviar resultado de vuelta al bot
        await self.queue.publish('cv.processed', {
            'whatsappId': message['whatsappId'],
            'result': {
                'summary': cv_data.summary,
                'match_score': cv_data.score
            }
        })

# Configuración de FastAPI
app = FastAPI()
message_queue = RabbitMQ()

@app.on_event("startup")
async def startup():
    await message_queue.subscribe('cv.received', 
                                CVProcessor().process_cv)
```

### 4. Message Queue (RabbitMQ)
- Comunicación asíncrona entre servicios
- Garantía de entrega de mensajes
- Manejo de picos de carga
- Reintentos automáticos

## Implementación

### 1. Flujos Principales
- Bienvenida y orientación
- Recepción de CV
- Preguntas frecuentes
- Seguimiento de proceso
- Retroalimentación

### 2. Procesamiento de Mensajes
```typescript
// Manejo de mensajes entrantes
adapterProvider.server.post('/v1/messages', handleCtx(async (bot, req, res) => {
    const { number, message, attachments } = req.body
    
    if (attachments?.length > 0) {
        // Procesar CV adjunto
        await handleCVUpload(attachments[0], number)
    } else {
        // Procesar mensaje normal
        await bot.sendMessage(number, await processUserMessage(message))
    }
    
    return res.end('processed')
}))
```

### 3. Integración con IA
```typescript
const cvAnalysisFlow = addKeyword('analizar')
    .addAction(async (ctx, { flowDynamic }) => {
        // Integrar con nuestro stack de IA
        const analysis = await analyzeCV(ctx.cvId)
        const summary = await generateCVSummary(analysis)
        await flowDynamic(summary)
    })
```

## Consecuencias

### Positivas
- Implementación rápida
- API bien documentada
- Soporte para múltiples proveedores
- Escalable y extensible
- Manejo robusto de eventos
- Separación clara de responsabilidades
- Cada servicio en su lenguaje óptimo
- Escalabilidad independiente
- Resiliencia mejorada

### Negativas
- Dependencia de WhatsApp Business API
- Limitaciones de API de WhatsApp
- Necesidad de manejar rate limits
- Gestión de sesiones
- Complejidad de infraestructura
- Necesidad de orquestación
- Latencia adicional
- Mantenimiento de dos stacks

### Mitigaciones
1. **Rate Limits**:
   - Queue de mensajes
   - Retry con backoff
   - Monitoreo de límites

2. **Sesiones**:
   - Cache distribuido
   - Estado persistente
   - Recuperación de errores

3. **Disponibilidad**:
   - Healthchecks
   - Logs detallados
   - Sistema de alertas

4. **Complejidad**:
   - Docker Compose para desarrollo
   - Kubernetes para producción
   - Monitoreo centralizado
   - Logs unificados

5. **Latencia**:
   - Optimización de colas
   - Caché distribuido
   - Conexiones persistentes
   - Batch processing

6. **Mantenimiento**:
   - CI/CD separados
   - Testing end-to-end
   - Documentación detallada
   - Métricas por servicio

## Referencias
- BuilderBot Documentation
- WhatsApp Business API
- Clean Architecture Guidelines
- Event-Driven Design Patterns
- FastAPI Documentation
- RabbitMQ Documentation
