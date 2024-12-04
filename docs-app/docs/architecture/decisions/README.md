# Decisiones de Arquitectura

Este directorio contiene los registros de decisiones de arquitectura (ADR) para el proyecto de sistema de reclutamiento.

## ¿Qué es un ADR?

Un ADR es un documento que captura una decisión arquitectónica importante junto con su contexto y consecuencias. Es una manera de documentar las decisiones técnicas significativas tomadas en el proyecto.

## Formato

Cada ADR sigue este formato:
1. **Título**: Breve y descriptivo
2. **Estado**: Propuesto, Aceptado, Deprecado, Reemplazado
3. **Contexto**: El problema que llevó a la decisión
4. **Decisión**: La solución elegida
5. **Consecuencias**: Impacto positivo y negativo
6. **Referencias**: Enlaces y documentación relevante

## Índice de ADRs

### Fundamentales
1. [Adoptar Clean Architecture y DDD](0001-adopt-clean-architecture.md)
   - Estructura base del proyecto
   - Principios arquitectónicos
   - Organización de código

2. [Usar ULID como Identificador](0002-use-ulid-as-identifier.md)
   - Sistema de identificadores
   - Ventajas sobre UUID
   - Implementación técnica

### Técnicos
3. [Desarrollo Async-First](0003-async-first-development.md)
   - Programación asíncrona
   - Manejo de concurrencia
   - Background tasks

4. [Integración con OpenAI](0004-openai-integration.md)
   - Análisis de CV con IA
   - Configuración del modelo
   - Manejo de prompts

## Convenciones de Nombrado

Los archivos ADR siguen estas convenciones:
1. Nombres en minúsculas con guiones
2. Prefijo numérico de 4 dígitos
3. Extensión .md

Ejemplo: `0001-adopt-clean-architecture.md`

## Mantenimiento

- Los ADRs son inmutables una vez aceptados
- Nuevas decisiones crean nuevos ADRs
- Los cambios se registran como nuevos ADRs que referencian los anteriores
- El estado se actualiza para reflejar deprecación o reemplazo
