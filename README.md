# Foolbank Volunteers API

Una API RESTful desarrollada con FastAPI que proporciona endpoints básicos para operaciones de prueba.

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
pip install -r requirements.txt
```

## 📚 Requisitos

- Python 3.7 o superior
- FastAPI
- Uvicorn (para ejecutar el servidor)

## 🏃‍♂️ Ejecución

Para ejecutar el servidor de desarrollo:
```bash
uvicorn FastApi.main:app --reload
```

El servidor estará disponible en `http://localhost:8000`

## 📚 Documentación de la API

La API incluye los siguientes endpoints:

### 1. Root Endpoint
- **URL**: `/`
- **Método**: GET
- **Respuesta**: "Hello World"

### 2. ID Endpoint
- **URL**: `/id/{id}`
- **Método**: GET
- **Parámetros**:
  - `id`: número entero
- **Respuesta**: Retorna el ID sumado a 10

### 3. Login Endpoint
- **URL**: `/login/{nombre}/{apellido}/{edad}`
- **Método**: GET
- **Parámetros**:
  - `nombre`: nombre del usuario
  - `apellido`: apellido del usuario
  - `edad`: edad del usuario
- **Respuesta**: Retorna un mensaje de bienvenida con el nombre, apellido y edad del usuario

## 🛠️ Documentación Interactiva

FastAPI genera automáticamente documentación interactiva:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📝 Licencia

Este proyecto está bajo la licencia MIT.

