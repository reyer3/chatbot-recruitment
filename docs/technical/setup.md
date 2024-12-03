# Guía de Instalación

## Requisitos Previos

### Software Base
- Python 3.11+
- Node.js 18+
- Docker y Docker Compose
- Make (opcional, para comandos simplificados)
- Git

### Servicios Externos
- Cuenta de OpenAI (API key)
- WhatsApp Business API
- PostgreSQL
- RabbitMQ

## Instalación

### 1. Clonar el Repositorio
```bash
git clone [URL_REPOSITORIO]
cd recruitment-system
```

### 2. Configuración de Entorno

#### Core Backend (Python)
```bash
# Crear entorno virtual
cd services/core
python -m venv venv
source venv/bin/activate  # En Windows: .\venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Dependencias de desarrollo
```

#### WhatsApp Service (Node.js)
```bash
cd services/whatsapp
npm install
```

#### Shared Kernel
```bash
cd shared
# Python
pip install -e python/
# Node.js
cd typescript && npm install
```

### 3. Variables de Entorno

Copiar los archivos de ejemplo y configurar:
```bash
# Core Backend
cp services/core/.env.example services/core/.env

# WhatsApp Service
cp services/whatsapp/.env.example services/whatsapp/.env
```

Variables requeridas:
```env
# Core Backend (.env)
DATABASE_URL=postgresql://user:pass@localhost:5432/recruitment
OPENAI_API_KEY=sk-...
RABBITMQ_URL=amqp://guest:guest@localhost:5672/
JWT_SECRET=your-secret-key

# WhatsApp Service (.env)
WHATSAPP_API_TOKEN=your-token
WHATSAPP_VERIFY_TOKEN=your-verify-token
RABBITMQ_URL=amqp://guest:guest@localhost:5672/
```

### 4. Servicios Locales con Docker

```bash
# Iniciar servicios
docker-compose up -d postgres rabbitmq

# Verificar estado
docker-compose ps
```

### 5. Migraciones de Base de Datos

```bash
cd services/core
alembic upgrade head
```

## Verificación de Instalación

### 1. Core Backend
```bash
cd services/core
pytest  # Ejecutar tests
uvicorn app.main:app --reload  # Iniciar servidor
```

### 2. WhatsApp Service
```bash
cd services/whatsapp
npm test  # Ejecutar tests
npm run dev  # Iniciar servidor
```

### 3. Verificar APIs
```bash
# Core Backend
curl http://localhost:8000/health

# WhatsApp Service
curl http://localhost:3000/health
```

## Problemas Comunes

### 1. Conexión a PostgreSQL
- Verificar que PostgreSQL esté corriendo: `docker-compose ps`
- Comprobar credenciales en `.env`
- Verificar que la base de datos existe

### 2. RabbitMQ
- Verificar que RabbitMQ esté corriendo: `docker-compose ps`
- Comprobar la interfaz web: `http://localhost:15672`
- Verificar conexiones en `.env`

### 3. Python/Node.js
- Verificar versiones: `python --version`, `node --version`
- Comprobar entorno virtual activo (Python)
- Verificar instalación de dependencias

## Siguientes Pasos

1. Revisar [Guía de Desarrollo](./development.md)
2. Configurar [IDE](./development.md#ide-setup)
3. Ejecutar [Tests](./testing.md)
4. Leer [Guía de Contribución](./contributing.md)
