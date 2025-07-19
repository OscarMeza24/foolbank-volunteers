# FoolBank Volunteers - API REST/GraphQL con FastAPI

Este proyecto implementa una API REST y GraphQL para la gestión de voluntarios de FoolBank, utilizando FastAPI, SQLAlchemy y Strawberry GraphQL. La aplicación utiliza SQLite como base de datos para facilitar la configuración y el desarrollo.

## Características Principales

- **API RESTful** completa con FastAPI
- **GraphQL** integrado con Strawberry
- **Base de datos** SQLite con SQLAlchemy ORM
- **Docker** para un despliegue consistente
- **Validación de datos** integrada con Pydantic
- **Documentación automática** con Swagger UI y ReDoc

## Estructura del Proyecto

```
FastApi/
├── app/
│   ├── database/       # Configuración de la base de datos
│   ├── graphql/        # Schemas y resolvers de GraphQL
│   ├── models/         # Modelos de SQLAlchemy
│   └── routers/        # Rutas de la API REST
├── .dockerignore
├── .gitignore
├── docker-compose.yml  # Configuración de Docker Compose
├── Dockerfile         # Configuración del contenedor
├── main.py            # Punto de entrada de la aplicación
└── requirements.txt   # Dependencias del proyecto
```

## Empezando

### Prerrequisitos

- Python 3.9 o superior
- Docker y Docker Compose (opcional, para despliegue con contenedores)

### Instalación Local

1. Clona el repositorio:
   ```bash
   git clone https://github.com/OscarMeza24/foolbank-volunteers.git
   cd FoolBank-Volunteers/FastApi
   ```

2. Crea y activa un entorno virtual:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # Linux/MacOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Inicia la aplicación:
   ```bash
   uvicorn main:app --reload
   ```

5. Abre tu navegador en:
   - API REST: http://localhost:8000
   - Documentación Swagger UI: http://localhost:8000/docs
   - Documentación ReDoc: http://localhost:8000/redoc
   - GraphQL Playground: http://localhost:8000/graphql

### Usando Docker

#### Requisitos
- Docker
- Docker Compose

#### Pasos para ejecutar con Docker

1. Construye y levanta los contenedores:
   ```bash
   docker-compose up --build
   ```

2. La aplicación estará disponible en:
   - API: http://localhost:8000
   - Documentación: http://localhost:8000/docs

3. Para detener los contenedores:
   ```bash
   docker-compose down
   ```

## Documentación de la API

La documentación interactiva está disponible en:
- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`
- **GraphQL Playground**: `/graphql`

## Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
DATABASE_URL=sqlite+aiosqlite:///./sqlite.db
```

## Contribución

1. Haz un Fork del proyecto
2. Crea tu rama de características (`git checkout -b feature/AmazingFeature`)
3. Haz commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Haz push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## Contacto

Oscar Meza - omeza2403@gmail.com

Enlace del Proyecto: [https://github.com/OscarMeza24/foolbank-volunteers](https://github.com/OscarMeza24/foolbank-volunteers)
