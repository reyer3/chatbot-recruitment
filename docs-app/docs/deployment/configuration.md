# Configuración y Despliegue

## Requisitos del Sistema

### Python y Dependencias
```bash
# Python 3.11+
python --version
Python 3.11.0

# Dependencias principales
pip install -r requirements.txt
```

### requirements.txt
```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.1
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9
python-multipart==0.0.6
openai==1.3.3
python-jose==3.3.0
passlib==1.7.4
redis==5.0.1
celery==5.3.4
boto3==1.29.3
pytest==7.4.3
pytest-asyncio==0.21.1
mypy==1.7.0
black==23.10.1
isort==5.12.0
```

## Variables de Entorno

### API
```env
# Server
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4
DEBUG=False
API_PREFIX=/api/v1
CORS_ORIGINS=["http://localhost:3000"]

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/recruitment
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=2000

# Storage
STORAGE_TYPE=s3
AWS_BUCKET_NAME=recruitment-cvs
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=us-east-1

# Authentication
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=1440  # 24 hours

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

### Workers
```env
# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1
CELERY_TASK_SERIALIZER=json
CELERY_RESULT_SERIALIZER=json

# Processing
MAX_CONCURRENT_ANALYSIS=5
ANALYSIS_TIMEOUT=300  # seconds
```

## Docker

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run migrations
RUN alembic upgrade head

EXPOSE 8000

CMD ["uvicorn", "src.apps.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/recruitment
      - CELERY_BROKER_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./:/app
    command: uvicorn src.apps.api.main:app --host 0.0.0.0 --port 8000 --reload

  worker:
    build: .
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/recruitment
      - CELERY_BROKER_URL=redis://redis:6379/0
    depends_on:
      - redis
      - db
    command: celery -A src.apps.workers.celery_app worker --loglevel=info

  db:
    image: postgres:14-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=recruitment
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

## Base de Datos

### Migraciones con Alembic
```python
# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from alembic import context
from src.contexts.shared.infrastructure.persistence.models import Base

config = context.config
target_metadata = Base.metadata

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()
```

### Índices
```sql
-- Búsqueda de texto completo en CVs
CREATE INDEX idx_cv_content ON cvs USING gin(to_tsvector('spanish', content));

-- Búsqueda por estado de candidato
CREATE INDEX idx_candidate_status ON candidates(status);

-- Búsqueda compuesta por proceso
CREATE INDEX idx_candidate_process ON candidates(process_id, status);
```

## CI/CD

### GitHub Actions
```yaml
name: CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          
      - name: Run type checking
        run: mypy src
        
      - name: Run tests
        run: |
          pytest tests/
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test
          
  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to production
        # Pasos de despliegue
```

## Monitoreo

### Métricas con Prometheus
```python
from prometheus_client import Counter, Histogram
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# Métricas personalizadas
cv_processing_duration = Histogram(
    'cv_processing_duration_seconds',
    'Time spent processing CVs'
)

cv_analysis_errors = Counter(
    'cv_analysis_errors_total',
    'Total number of CV analysis errors'
)

# Instrumentación automática
Instrumentator().instrument(app).expose(app)
```

### Logging
```python
import logging
import structlog

def setup_logging():
    logging.basicConfig(
        format="%(message)s",
        level=logging.INFO,
    )
    
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_log_level,
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

logger = structlog.get_logger()
```

## Backups

### Base de Datos
```python
import subprocess
from datetime import datetime

def backup_database():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f'backup_{timestamp}.dump'
    
    # Crear backup
    subprocess.run([
        'pg_dump',
        '-Fc',
        '-h', 'localhost',
        '-U', 'user',
        '-d', 'recruitment',
        '-f', backup_file
    ])
    
    # Subir a S3
    subprocess.run([
        'aws', 's3', 'cp',
        backup_file,
        f's3://recruitment-backups/{backup_file}'
    ])
```

### Archivos
```python
import boto3
from datetime import datetime

def backup_files():
    s3 = boto3.client('s3')
    timestamp = datetime.now().strftime('%Y/%m/%d')
    
    # Copiar CVs a bucket de backup
    s3.sync(
        's3://recruitment-cvs',
        f's3://recruitment-backups/cvs/{timestamp}'
    )
