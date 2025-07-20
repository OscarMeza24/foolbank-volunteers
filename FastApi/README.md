# FoolBank Volunteers - API REST/GraphQL con FastAPI

API moderna y eficiente para la gestión de voluntarios de FoolBank, construida con FastAPI, SQLAlchemy y Strawberry GraphQL. La aplicación utiliza SQLite en desarrollo y soporta múltiples bases de datos para producción.

## Características Principales

- **API RESTful** completa con FastAPI
- **GraphQL** integrado con Strawberry
- **Base de datos** SQLite con SQLAlchemy ORM (soporte para PostgreSQL/MySQL)
- **Autenticación JWT** para endpoints protegidos
- **WebSockets** para comunicación en tiempo real
- **Docker** para un despliegue consistente
- **Validación de datos** con Pydantic v2
- **Documentación automática** con Swagger UI y ReDoc
- **Sistema de logs** estructurado
- **Variables de entorno** para configuración flexible
- **CORS** habilitado para integración con frontend

## Estructura del Proyecto

```
FastApi/
├── app/
│   ├── api/            # Endpoints de la API REST
│   ├── core/           # Configuraciones centrales
│   ├── database/       # Configuración de la base de datos
│   ├── graphql/        # Schemas y resolvers de GraphQL
│   ├── models/         # Modelos de SQLAlchemy
│   ├── routers/        # Rutas de la API REST
│   ├── schemas/        # Esquemas Pydantic
│   ├── services/       # Lógica de negocio
│   ├── tests/          # Pruebas unitarias e integración
│   └── websocket/      # Handlers de WebSocket
├── .env.example        # Variables de entorno de ejemplo
├── .gitignore
├── alembic/            # Migraciones de base de datos
├── docker-compose.yml  # Configuración de Docker Compose
├── Dockerfile         # Configuración del contenedor
├── main.py            # Punto de entrada de la aplicación
├── pyproject.toml     # Configuración de proyecto y dependencias
└── requirements.txt   # Dependencias del proyecto
```

## Empezando

### Prerrequisitos

- Python 3.10 o superior
- Docker y Docker Compose (recomendado)
- Git (para control de versiones)

### Instalación Local

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/OscarMeza24/foolbank-volunteers.git
   cd FoolBank-Volunteers/FastApi
   ```

2. **Configura el entorno virtual**:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # Linux/MacOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura las variables de entorno**:
   ```bash
   cp .env.example .env
   # Edita el archivo .env según sea necesario
   ```

5. **Inicia la aplicación**:
   ```bash
   uvicorn main:app --reload
   ```

6. **Accede a la documentación**:
   - API REST: http://localhost:8000
   - Documentación Swagger UI: http://localhost:8000/docs
   - Documentación ReDoc: http://localhost:8000/redoc
   - GraphQL Playground: http://localhost:8000/graphql

### Usando Docker

1. **Construye y levanta los contenedores**:
   ```bash
   docker-compose up --build
   ```

2. **La aplicación estará disponible en**:
   - API: http://localhost:8000
   - Documentación: http://localhost:8000/docs

3. **Comandos útiles**:
   ```bash
   # Detener contenedores
   docker-compose down
   
   # Ver logs
   docker-compose logs -f
   
   # Ejecutar migraciones
   docker-compose exec web alembic upgrade head
   ```

## Documentación de la API

La documentación interactiva está disponible en:
- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`
- **GraphQL Playground**: `/graphql`

### Autenticación

La API utiliza JWT para autenticación. Para acceder a endpoints protegidos:

1. Obtén un token de autenticación:
   ```bash
   curl -X 'POST' \
     'http://localhost:8000/api/auth/token' \
     -H 'accept: application/json' \
     -H 'Content-Type: application/x-www-form-urlencoded' \
     -d 'username=tu_usuario&password=tu_contraseña'
   ```

2. Usa el token en las cabeceras de tus solicitudes:
   ```
   Authorization: Bearer tu_token_jwt
   ```

## Ejecutando Pruebas

Para ejecutar las pruebas unitarias:

```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Ejecutar pruebas
pytest

# Con cobertura de código
pytest --cov=app tests/
```

## Variables de Entorno

Las siguientes variables pueden configurarse en el archivo `.env`:

```env
# Configuración de la aplicación
APP_ENV=development
DEBUG=True
SECRET_KEY=tu_clave_secreta_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Base de datos
DATABASE_URL=sqlite:///./sql_app.db
# Para producción:
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

## Contribución

1. Haz un Fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Haz commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Haz push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contacto

Oscar Meza - omeza2411@gmail.com

Enlace del Proyecto: [https://github.com/OscarMeza24/foolbank-volunteers](https://github.com/OscarMeza24/foolbank-volunteers)
