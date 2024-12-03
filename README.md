# ChatBot de Reclutamiento

Sistema automatizado para el análisis y evaluación de CVs utilizando OpenAI.

## Descripción
Sistema que automatiza el proceso de evaluación de currículums recibidos de portales laborales, utilizando IA para analizar y clasificar candidatos según los requisitos específicos de cada proceso de selección activo.

## Características Principales
- Gestión de repositorio de CVs
- Análisis automático de CVs usando OpenAI
- Base de datos estructurada de candidatos
- Mantenedor de procesos de selección
- Sistema de evaluación basado en IA
- Panel de administración para RRHH

## Flujo del Sistema
1. El equipo de RRHH sube los CVs recibidos al repositorio
2. El sistema analiza automáticamente cada CV
3. La información se estructura y almacena en la base de datos
4. Se realiza evaluación según criterios del proceso activo
5. Se generan reportes y rankings de candidatos

## Estructura de Datos
### Candidatos
- Nombre
- Teléfono
- Email
- Evaluación
- Razón Principal
- Aspectos Positivos
- Experiencia Relevante
- Habilidades Clave
- Match con Requisitos (%)

### Procesos de Selección
- Título del Puesto
- Descripción
- Requisitos
- Condiciones Laborales
- Criterios de Evaluación
- Estado del Proceso

## Estructura del Proyecto
recruitment-system/
├── docs/                     # Documentación del proyecto
│   ├── [architecture/](docs/architecture/system-design.md)        # Diseño y arquitectura
│   ├── [processes/](docs/processes/recruitment.md)          # Flujos de procesos
│   └── [integrations/](docs/integrations/openai-integration.md)       # Guías de integración
├── src/
│   ├── apps/               # Aplicaciones (API, Workers, etc)
│   │   ├── api/           # API REST
│   │   │   ├── routes/
│   │   │   └── server.ts
│   │   └── workers/       # Procesamiento en background
│   │       └── cv-processor/
│   │
│   ├── contexts/          # Bounded Contexts
│   │   ├── shared/       # Código compartido entre contextos
│   │   │   ├── domain/
│   │   │   │   ├── value-objects/
│   │   │   │   └── events/
│   │   │   └── infrastructure/
│   │   │       └── persistence/
│   │   │
│   │   ├── recruitment-processes/  # Contexto de Procesos de Selección
│   │   │   ├── application/       # Casos de uso
│   │   │   │   ├── create/
│   │   │   │   └── update/
│   │   │   ├── domain/           # Reglas de negocio
│   │   │   │   ├── process.ts
│   │   │   │   └── repository/
│   │   │   └── infrastructure/   # Implementaciones
│   │   │       ├── persistence/
│   │   │       └── services/
│   │   │
│   │   ├── cv-analysis/          # Contexto de Análisis de CVs
│   │   │   ├── application/
│   │   │   │   ├── analyze/
│   │   │   │   └── evaluate/
│   │   │   ├── domain/
│   │   │   │   ├── cv.ts
│   │   │   │   └── services/
│   │   │   └── infrastructure/
│   │   │       ├── openai/
│   │   │       └── storage/
│   │   │
│   │   └── candidates/           # Contexto de Candidatos
│   │       ├── application/
│   │       ├── domain/
│   │       └── infrastructure/
│   │
│   └── shared-kernel/           # Kernel compartido
│       ├── domain/
│       └── infrastructure/
│
├── tests/                    # Pruebas
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
└── README.md

## Tecnologías
- OpenAI API (Análisis de CVs)
- Base de datos PostgreSQL
- FastAPI (Backend)
- React (Frontend Admin)

## Instalación
[Pendiente]

## Configuración
[Pendiente]

## Licencia
[Pendiente]
