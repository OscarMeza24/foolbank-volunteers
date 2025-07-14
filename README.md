# Proyecto de FastAPI, SQLAlchemy y GraphQL

Este proyecto demuestra la integración entre FastAPI, SQLAlchemy y Strawberry GraphQL, utilizando una base de datos SQLite3. El objetivo es mostrar la sinergia y capacidades de estas tecnologías cuando se combinan.

## Características Principales

- **Integración FastAPI:** Utiliza FastAPI, un moderno framework web rápido para construir APIs con Python 3.7+.

- **Base de Datos SQLAlchemy:** Utiliza SQLAlchemy, una poderosa herramienta SQL y biblioteca de mapeo objeto-relacional.

- **GraphQL con Strawberry:** Implementa Strawberry, una biblioteca GraphQL para Python con enfoque en código primero.

- **Base de Datos SQLite3:** Utiliza SQLite3 como base de datos backend para facilitar la configuración y portabilidad.

## Comenzando

Sigue estos pasos para descargar, instalar los requisitos y comenzar el servidor FastAPI:

### Requisitos Previos

- Asegúrate de tener Python 3.7 o superior instalado.

### Descarga e Instalación del Proyecto

1. Clona el repositorio:

   ```git clone https://github.com/your-username/your-fastapi-project.git```

2. Cambia al directorio del proyecto:

   ```cd foodbank-Voluntatios-Proyecto```

3. Crea y activa un entorno virtual:

   ```python -m venv venv```
   
   ```source venv/bin/activate```
   #### En Windows, usa
   ```venv\Scripts\activate```

4. Instala las dependencias:

   ```pip install -r requirements.txt```

### Iniciar el Servidor FastAPI

Inicia el servidor FastAPI con el siguiente comando:

   ```uvicorn main:app --reload```

Visita http://127.0.0.1:8000/docs en tu navegador para acceder a la documentación de Swagger y explorar los endpoints de la API disponibles.

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

Result:

```
{
  "data": {
    "updateHeader": {
      "name": "Mutation Update",
      "salesRepId": 105,
      "buyerId": 1002,
      "active": "N"
    }
  }
}
```


### Insert:

```
mutation MyMutation {
  createHeader(
    header: {headerId: 7, name: "TEST", buyerId: 1002, active: "Y", salesRepId: 105}
  ) {
    name
    salesRepId
    buyerId
    active
  }
}
```



![image](https://github.com/tyanakiev/graphql-fastapi/assets/5628399/d091ba9b-24d4-44d8-9eaf-c29edbd46a81)
