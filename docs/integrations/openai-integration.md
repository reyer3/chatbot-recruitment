# Integración con OpenAI

## Funcionalidades

### 1. Análisis de CV
- Extracción de información clave
- Identificación de habilidades
- Evaluación de experiencia
- Detección de palabras clave

### 2. Evaluación de Respuestas
- Análisis de respuestas a preguntas abiertas
- Evaluación de coherencia
- Detección de red flags

### 3. Generación de Preguntas
- Preguntas personalizadas basadas en CV
- Adaptación según el perfil del puesto
- Seguimiento contextual

## Implementación

### Modelos a Utilizar
1. **GPT-4**
   - Análisis profundo de texto
   - Generación de preguntas
   - Evaluación de respuestas

2. **GPT-3.5-turbo**
   - Interacciones rápidas
   - Respuestas simples
   - Procesamiento inicial

### Prompts Base
```plaintext
# Análisis de CV
Analiza el siguiente CV y extrae:
1. Experiencia relevante
2. Habilidades técnicas
3. Habilidades blandas
4. Formación académica
5. Logros destacados

# Evaluación de Ajuste
Evalúa el ajuste del candidato para [PUESTO] considerando:
1. Requisitos mínimos
2. Experiencia requerida
3. Habilidades necesarias
```

## Consideraciones de Seguridad
- Manejo seguro de datos personales
- Límites de uso de API
- Almacenamiento de resultados
- Cumplimiento de GDPR/LGPD
