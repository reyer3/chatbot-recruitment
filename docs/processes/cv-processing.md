# Procesamiento de CVs

## Flujo de Procesamiento

### 1. Preparación
- Conversión de CV a texto (PDF/Word → texto plano)
- Limpieza y normalización de datos
- Extracción de metadatos básicos

### 2. Análisis con OpenAI

#### Prompt Base para Análisis de CV
```plaintext
Analiza el siguiente CV y extrae la información en formato JSON con la siguiente estructura:

{
    "datos_personales": {
        "nombre": "",
        "telefono": "",
        "email": ""
    },
    "experiencia_relevante": [
        {
            "empresa": "",
            "cargo": "",
            "periodo": "",
            "responsabilidades_key": []
        }
    ],
    "habilidades": {
        "tecnicas": [],
        "blandas": []
    },
    "educacion": [
        {
            "titulo": "",
            "institucion": "",
            "año": ""
        }
    ],
    "logros_destacados": []
}

CV a analizar:
[CONTENIDO_CV]
```

#### Prompt de Evaluación
```plaintext
Evalúa el siguiente perfil para el puesto de [PUESTO] según estos criterios:

Requisitos del puesto:
[REQUISITOS]

Condiciones:
[CONDICIONES]

Perfil del candidato:
[PERFIL_JSON]

Genera una evaluación en formato JSON con:
{
    "evaluacion_numerica": 0-100,
    "razon_principal": "",
    "aspectos_positivos": [],
    "aspectos_mejorables": [],
    "match_requisitos": 0-100,
    "recomendacion": "APROBAR|REVISAR|RECHAZAR"
}
```

### 3. Estructuración de Datos
- Normalización de resultados
- Validación de datos extraídos
- Enriquecimiento de información

### 4. Almacenamiento
- Registro en base de datos
- Indexación para búsqueda
- Vinculación con proceso de selección

## Configuración de Procesos

### Definición de Proceso
```json
{
    "titulo": "Desarrollador Frontend Senior",
    "descripcion": "Buscamos desarrollador frontend con experiencia...",
    "requisitos": [
        "5+ años de experiencia en React",
        "Conocimientos de TypeScript",
        "Experiencia en testing"
    ],
    "condiciones": {
        "modalidad": "Híbrido",
        "ubicacion": "Santiago",
        "tipo_contrato": "Indefinido"
    },
    "criterios_evaluacion": {
        "experiencia_relevante": 40,
        "habilidades_tecnicas": 30,
        "habilidades_blandas": 15,
        "formacion": 15
    },
    "prompt_template": "Personalización específica del prompt..."
}
```

## Métricas y Reportes
- Tasa de procesamiento exitoso
- Distribución de evaluaciones
- Tiempo promedio de procesamiento
- Precisión de extracción de datos
