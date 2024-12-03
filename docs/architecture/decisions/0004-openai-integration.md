# 4. Integración con OpenAI

Fecha: 2023-11-15

## Estado

Aceptado

## Contexto

Necesitamos un sistema de análisis de CV que:
- Extraiga información relevante
- Evalúe candidatos objetivamente
- Genere recomendaciones detalladas
- Sea adaptable a diferentes roles

## Decisión

Utilizaremos la API de OpenAI con GPT-4 por:

1. **Capacidades del Modelo**:
   - Comprensión de contexto superior
   - Análisis multilingüe
   - Extracción precisa de información
   - Evaluación consistente

2. **Implementación**:
   - API REST moderna
   - SDK oficial para Python
   - Rate limiting incluido
   - Manejo de errores robusto

3. **Modelo Específico**: GPT-4
   - Mayor precisión que GPT-3.5
   - Mejor comprensión de contexto
   - Capacidad de seguir instrucciones complejas
   - Análisis más detallado

## Implementación

### Prompt Template
```python
class CVAnalysisPrompt:
    @staticmethod
    def create(cv_text: str, requirements: List[str]) -> str:
        return f"""
        Analiza el siguiente CV para el puesto que requiere:
        {requirements}

        CV:
        {cv_text}

        Proporciona una evaluación estructurada incluyendo:
        1. Coincidencia con requisitos
        2. Años de experiencia relevante
        3. Habilidades técnicas
        4. Recomendaciones
        """
```

### Servicio de Análisis
```python
class OpenAICVAnalyzer:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    async def analyze(
        self,
        cv_text: str,
        requirements: List[str]
    ) -> dict:
        prompt = CVAnalysisPrompt.create(cv_text, requirements)
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Eres un experto en RRHH..."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        
        return self._parse_response(response)
```

### Manejo de Rate Limits
```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential
)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def analyze_with_retry(
    analyzer: OpenAICVAnalyzer,
    cv_text: str,
    requirements: List[str]
) -> dict:
    return await analyzer.analyze(cv_text, requirements)
```

## Consecuencias

### Positivas
- Análisis de alta calidad
- Rápida implementación
- Actualizaciones automáticas del modelo
- Flexibilidad en evaluación

### Negativas
- Costo por uso
- Dependencia de servicio externo
- Latencia en respuestas
- Necesidad de prompt engineering

### Mitigaciones
1. **Costos**:
   - Caché de resultados
   - Batch processing
   - Monitoreo de uso

2. **Disponibilidad**:
   - Circuit breaker
   - Fallback local
   - Reintentos inteligentes

3. **Latencia**:
   - Procesamiento asíncrono
   - Análisis en background
   - Resultados parciales

## Referencias
- OpenAI API Documentation
- GPT-4 Technical Report
- Rate Limiting Best Practices
