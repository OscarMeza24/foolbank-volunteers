# Foolbank Volunteers API

Una API desarrollada con FastAPI que proporciona endpoints REST y GraphQL para operaciones de prueba y gestión de usuarios.

## 🚀 Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/OscarMeza24/foolbank-volunteers.git
cd foolbank-volunteers
```

2. Crea y activa un entorno virtual (opcional pero recomendado):
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
```

3. Instala las dependencias:
```bash
pip install -r FastApi/requirements.txt
```

## 📚 Requisitos

- Python 3.7 o superior
- FastAPI
- Uvicorn
- SQLAlchemy
- Graphene y graphene-sqlalchemy

## 🏃‍♂️ Ejecución

Para ejecutar el servidor de desarrollo:
```bash
uvicorn FastApi.app.main:app --reload
```

El servidor estará disponible en `http://localhost:8000`

## 📦 Estructura del Proyecto

```
FastApi/
  app/
    main.py                # Archivo principal de la API
    database/
      database.py          # Configuración de la base de datos SQLAlchemy
    graphql/
      schema.py            # Esquema GraphQL (consultas y tipos)
    models/
      user.py              # Modelo User de SQLAlchemy
```

## 🚦 Endpoints REST

- **GET /**  
  Mensaje de bienvenida.

- **POST /users**  
  Crea un usuario.  
  **Body:**  
  ```json
  {
    "name": "Nombre",
    "last_name": "Apellido",
    "age": 25
  }
  ```
  **Respuesta:**  
  Objeto usuario creado.

## 🔎 Endpoint GraphQL

- **POST /graphql**  
  Permite realizar consultas y mutaciones GraphQL.

  Ejemplo de consulta:
  ```graphql
  query {
    users {
      id
      name
      last_name
      age
    }
  }
  ```

  Ejemplo de consulta individual:
  ```graphql
  query {
    user(id: 1) {
      name
      last_name
      age
    }
  }
  ```

## 🗄️ Base de Datos

- Utiliza SQLite por defecto (`test.db`).
- El modelo principal es `User` con los campos: `id`, `name`, `last_name`, `age`.

## 🛠️ Documentación Interactiva

FastAPI genera automáticamente documentación interactiva:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📄 Notas

- El endpoint `/graphql` soporta métodos GET y POST.
- El modelo `User` está preparado para relacionarse con un modelo `Post`, pero actualmente no existe el modelo `Post` en el proyecto.
- El archivo [FastApi/app/graphql/schema.py](FastApi/app/graphql/schema.py) contiene la definición de los esquemas y resolvers de GraphQL.

## 📝 Licencia

Este proyecto está bajo la licencia MIT.

