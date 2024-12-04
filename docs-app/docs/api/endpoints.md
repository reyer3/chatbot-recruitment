# API Endpoints

## Autenticación

### POST /api/v1/auth/login
Autenticación de usuarios.

```python
from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
```

**Request:**
```json
{
    "email": "admin@example.com",
    "password": "secure_password"
}
```

**Response:**
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer"
}
```

## Procesos de Reclutamiento

### POST /api/v1/recruitment-processes
Crear un nuevo proceso de reclutamiento.

```python
from pydantic import BaseModel
from typing import List

class CreateProcessRequest(BaseModel):
    title: str
    description: str
    requirements: List[str]
    evaluation_criteria: dict[str, float]

class ProcessResponse(BaseModel):
    id: str  # ULID string, ej: "01ARZ3NDEKTSV4RRFFQ69G5FAV"
    title: str
    description: str
    requirements: List[str]
    evaluation_criteria: dict[str, float]
    status: str
    created_at: datetime
```

**Request:**
```json
{
    "title": "Senior Python Developer",
    "description": "Buscamos desarrollador Python con experiencia en FastAPI",
    "requirements": [
        "5+ años de experiencia en Python",
        "Conocimiento de FastAPI",
        "Experiencia en arquitectura limpia"
    ],
    "evaluation_criteria": {
        "technical_skills": 0.4,
        "experience": 0.3,
        "soft_skills": 0.3
    }
}
```

### GET /api/v1/recruitment-processes/{process_id}
Obtener detalles de un proceso específico.

**Response:**
```json
{
    "id": "01ARZ3NDEKTSV4RRFFQ69G5FAV",
    "title": "Senior Python Developer",
    "description": "Buscamos desarrollador Python con experiencia en FastAPI",
    "requirements": [
        "5+ años de experiencia en Python",
        "Conocimiento de FastAPI",
        "Experiencia en arquitectura limpia"
    ],
    "evaluation_criteria": {
        "technical_skills": 0.4,
        "experience": 0.3,
        "soft_skills": 0.3
    },
    "status": "active",
    "created_at": "2023-11-15T14:30:00Z"
}
```

## Análisis de CV

### POST /api/v1/cv-analysis
Analizar un CV para un proceso específico.

```python
class CVAnalysisRequest(BaseModel):
    process_id: str  # ULID string
    cv_file: UploadFile
    candidate_info: dict[str, str]

class CVAnalysisResponse(BaseModel):
    analysis_id: str  # ULID string
    status: str
    matching_score: float
    evaluation_details: dict[str, float]
    recommendations: List[str]
```

**Request:**
```
POST /api/v1/cv-analysis
Content-Type: multipart/form-data

process_id: "01ARZ3NDEKTSV4RRFFQ69G5FAV"
cv_file: [binary_file]
candidate_info: {
    "name": "Juan Pérez",
    "email": "juan@example.com"
}
```

**Response:**
```json
{
    "analysis_id": "01ARZ3NDEKTSV4RRFFQ69G5FAV",
    "status": "completed",
    "matching_score": 0.85,
    "evaluation_details": {
        "technical_skills": 0.9,
        "experience": 0.8,
        "soft_skills": 0.85
    },
    "recommendations": [
        "Candidato altamente compatible con el perfil",
        "Experiencia técnica excepcional en Python",
        "Recomendado para entrevista técnica"
    ]
}
```

### GET /api/v1/cv-analysis/{analysis_id}
Obtener resultados de un análisis específico.

**Response:**
```json
{
    "analysis_id": "01ARZ3NDEKTSV4RRFFQ69G5FAV",
    "process_id": "01ARZ3NDEKTSV4RRFFQ69G5FAV",
    "candidate_id": "01ARZ3NDEKTSV4RRFFQ69G5FAV",
    "status": "completed",
    "matching_score": 0.85,
    "evaluation_details": {
        "technical_skills": 0.9,
        "experience": 0.8,
        "soft_skills": 0.85
    },
    "recommendations": [
        "Candidato altamente compatible con el perfil",
        "Experiencia técnica excepcional en Python",
        "Recomendado para entrevista técnica"
    ],
    "created_at": "2023-11-15T14:35:00Z",
    "completed_at": "2023-11-15T14:36:30Z"
}
```

## Candidatos

### GET /api/v1/candidates/{candidate_id}
Obtener información detallada de un candidato.

```python
class CandidateResponse(BaseModel):
    id: str  # ULID string
    name: str
    email: str
    status: str
    evaluations: List[EvaluationSummary]
    created_at: datetime
    updated_at: datetime

class EvaluationSummary(BaseModel):
    process_id: str  # ULID string
    matching_score: float
    status: str
    evaluation_date: datetime
```

**Response:**
```json
{
    "id": "01ARZ3NDEKTSV4RRFFQ69G5FAV",
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "status": "in_process",
    "evaluations": [
        {
            "process_id": "01ARZ3NDEKTSV4RRFFQ69G5FAV",
            "matching_score": 0.85,
            "status": "evaluated",
            "evaluation_date": "2023-11-15T14:36:30Z"
        }
    ],
    "created_at": "2023-11-15T14:35:00Z",
    "updated_at": "2023-11-15T14:36:30Z"
}
```

### PATCH /api/v1/candidates/{candidate_id}
Actualizar el estado de un candidato.

```python
class UpdateCandidateRequest(BaseModel):
    status: str
    notes: str | None = None

class UpdateCandidateResponse(BaseModel):
    id: str  # ULID string
    status: str
    updated_at: datetime
```

**Request:**
```json
{
    "status": "interviewed",
    "notes": "Excelente desempeño en la entrevista técnica"
}
```

**Response:**
```json
{
    "id": "01ARZ3NDEKTSV4RRFFQ69G5FAV",
    "status": "interviewed",
    "updated_at": "2023-11-15T16:30:00Z"
}
```

## Manejo de Errores

### Errores Comunes

```python
class ErrorResponse(BaseModel):
    code: str
    message: str
    details: dict[str, Any] | None = None
```

#### 400 Bad Request
```json
{
    "code": "INVALID_REQUEST",
    "message": "Datos de solicitud inválidos",
    "details": {
        "email": "formato de email inválido"
    }
}
```

#### 401 Unauthorized
```json
{
    "code": "UNAUTHORIZED",
    "message": "Token de autenticación inválido o expirado"
}
```

#### 404 Not Found
```json
{
    "code": "NOT_FOUND",
    "message": "Recurso no encontrado",
    "details": {
        "resource_type": "candidate",
        "resource_id": "invalid_id"
    }
}
```

#### 429 Too Many Requests
```json
{
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Demasiadas solicitudes",
    "details": {
        "retry_after": 60
    }
}
