# Diseño del Sistema

## Componentes Principales

### 1. Módulo de Gestión de CVs
- **Propósito**: Gestionar el repositorio de currículums
- **Responsabilidades**:
  - Carga masiva de CVs
  - Organización por proceso de selección
  - Extracción inicial de metadatos
  - Control de versiones de documentos

### 2. Procesador de CVs con IA
- **Propósito**: Análisis y extracción de información de CVs
- **Responsabilidades**:
  - Extracción de datos estructurados
  - Análisis de habilidades y experiencia
  - Evaluación según criterios del proceso
  - Generación de resúmenes y puntos clave

### 3. Gestor de Procesos de Selección
- **Propósito**: Administración de procesos activos
- **Responsabilidades**:
  - Mantenimiento de requisitos y descripciones
  - Gestión de criterios de evaluación
  - Configuración de prompts específicos
  - Seguimiento de estados del proceso

### 4. Base de Datos
- **Propósito**: Almacenamiento estructurado de información
- **Responsabilidades**:
  - Datos de candidatos
  - Procesos de selección
  - Evaluaciones y resultados
  - Histórico de cambios

### 5. Panel de Administración
- **Propósito**: Interfaz para equipo de RRHH
- **Responsabilidades**:
  - Gestión de procesos
  - Visualización de candidatos
  - Configuración de criterios
  - Reportes y estadísticas

## Flujo de Datos
1. Carga de CV → Repositorio
2. CV → Procesador de IA
3. Datos Estructurados → Base de Datos
4. Proceso de Selección → Criterios de Evaluación
5. Evaluación → Resultados en Panel Admin

## Modelo de Datos

### Candidatos
```sql
CREATE TABLE candidates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100),
    evaluation_score DECIMAL,
    main_reason TEXT,
    positive_aspects TEXT[],
    relevant_experience TEXT,
    key_skills TEXT[],
    requirements_match DECIMAL,
    cv_path VARCHAR(255),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Procesos de Selección
```sql
CREATE TABLE recruitment_processes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100),
    description TEXT,
    requirements TEXT[],
    conditions TEXT,
    evaluation_criteria JSONB,
    status VARCHAR(20),
    prompt_template TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

## Integraciones
- OpenAI API (GPT-4)
- Sistema de almacenamiento de archivos
- Sistema de autenticación
- Generador de reportes
