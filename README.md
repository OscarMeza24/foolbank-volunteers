# FoolBank - Sistema de Gestión de Voluntarios

Este proyecto es un sistema integral para la gestión de voluntarios, eventos y donaciones para FoolBank. Combina una API REST con GraphQL y WebSockets en tiempo real para ofrecer una experiencia completa de gestión de voluntariado.

## Características Principales

### Backend
- **FastAPI:** Framework web moderno y rápido para construir APIs con Python 3.7+.
- **SQLAlchemy:** ORM potente para la gestión de bases de datos relacionales.
- **GraphQL con Strawberry:** Implementación de GraphQL con enfoque en código primero.
- **WebSockets:** Soporte para comunicación en tiempo real entre clientes y servidor.

### Frontend
- **Interfaz React (próximamente):** Panel de administración moderno y responsivo.

### Base de Datos
- **SQLite3:** Base de datos ligera para desarrollo y pruebas.
- **PostgreSQL (producción):** Base de datos robusta para entornos de producción.

## 🚀 Comenzando

Sigue estos pasos para configurar el entorno de desarrollo y ejecutar la aplicación:

### Requisitos Previos

- Python 3.9 o superior
- Node.js 16+ (para el módulo WebSocket)
- npm o yarn
- Git

### Configuración del Entorno

1. Clona el repositorio:
   ```bash
   git clone https://github.com/OscarMeza24/foolbank-volunteers.git
   cd foolbank-volunteers
   ```

2. Configura el entorno de Python:
   ```bash
   # Crea y activa el entorno virtual
   python -m venv venv
   # En Windows
   .\venv\Scripts\activate
   # En Unix/macOS
   source venv/bin/activate

   # Instala dependencias de Python
   pip install -r FastApi/requirements.txt
   ```

3. Configura el módulo WebSocket:
   ```bash
   cd Modulo-Websocket
   npm install
   ```

### Ejecución

1. Inicia el servidor FastAPI:
   ```bash
   cd FastApi
   uvicorn main:app --reload
   ```

2. En otra terminal, inicia el servidor WebSocket:
   ```bash
   cd Modulo-Websocket
   npm run start:dev
   ```

## 📚 Documentación de la API

- **API REST:** http://localhost:8000/docs
- **GraphQL Playground:** http://localhost:8000/graphql
- **WebSocket:** ws://localhost:3000 (desde el módulo WebSocket)

## 🛠️ Estructura del Proyecto

```
foolbank-volunteers/
├── FastApi/                 # Backend principal con FastAPI
│   ├── app/
│   │   ├── api/            # Endpoints de la API
│   │   ├── core/            # Configuraciones principales
│   │   ├── db/              # Configuración de base de datos
│   │   ├── models/          # Modelos SQLAlchemy
│   │   ├── schemas/         # Esquemas Pydantic
│   │   └── websocket/       # Configuración de WebSockets
│   └── main.py              # Punto de entrada de la aplicación
│
└── Modulo-Websocket/        # Servidor WebSocket
    ├── src/
    │   ├── events/          # Controladores de eventos
    │   └── main.ts          # Punto de entrada
    └── test/                # Pruebas
```

## API GraphQL

### Acceder al Playground GraphQL

Visita http://127.0.0.1:8000/graphql en tu navegador para acceder al Playground GraphQL.

### Ejemplos de Consultas GraphQL

#### 1. Usuarios

```graphql
query GetUsuarios {
  usuarios {
    Usuarios_id
    nombre
    apellido
    correo
    telefono
    tipo
  }
}
```

#### 2. Voluntarios

```graphql
query GetVoluntarios {
  voluntarios {
    voluntarios_id
    nombre
    apellido
    correo
    telefono
    estado
  }
}
```

#### 3. Eventos

```graphql
query GetEventos {
  eventos {
    eventos_id
    nombre
    fecha
    hora
    lugar
    tipo
    estado
  }
}
```

#### 4. Asignaciones

```graphql
query GetAsignaciones {
  asignaciones {
    asignaciones_id
    evento_id
    voluntario_id
    estado
  }
}
```

#### 5. Feedback

```graphql
query GetFeedback {
  feedback {
    feedback_id
    evento_id
    voluntario_id
    calificacion
    comentario
  }
}
```

### Ejemplos de Mutaciones

#### 1. Crear Usuario

```graphql
mutation CreateUsuario {
  createUsuario(usuario: {
    nombre: "Juan"
    apellido: "Perez"
    correo: "juan@example.com"
    telefono: "123456789"
    tipo: "voluntario"
  }) {
    Usuarios_id
    nombre
    correo
  }
}
```

#### 2. Crear Evento

```graphql
mutation CreateEvento {
  createEvento(evento: {
    nombre: "Distribución de alimentos"
    fecha: "2025-07-15"
    hora: "14:00"
    lugar: "Plaza Central"
    tipo: "distribucion"
    estado: "pendiente"
  }) {
    eventos_id
    nombre
    fecha
  }
}
```

#### 3. Asignar Voluntario a Evento

```graphql
mutation CreateAsignacion {
  createAsignacion(asignacion: {
    evento_id: 1
    voluntario_id: 1
    estado: "confirmado"
  }) {
    asignaciones_id
    estado
  }
}
```

#### 4. Dar Feedback

```graphql
mutation CreateFeedback {
  createFeedback(feedback: {
    evento_id: 1
    voluntario_id: 1
    calificacion: 5
    comentario: "Excelente experiencia"
  }) {
    feedback_id
    calificacion
    comentario
  }
}
```

### Ejemplo de Consulta Compleja

```graphql
query GetEventosConVoluntarios {
  eventos {
    eventos_id
    nombre
    fecha
    lugar
    asignaciones {
      voluntario {
        nombre
        apellido
      }
      estado
    }
    feedback {
      voluntario {
        nombre
      }
      calificacion
      comentario
    }
  }
}
```
