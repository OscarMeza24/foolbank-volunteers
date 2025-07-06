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

#### Obtener Datos de Recursos

```graphql
query MyQuery {
  getHeaders {
    active
    buyerId
    headerId
    name
    salesRepId
    lines {
      creationDate
      headerId
      itemId
      lineId
      marketId
      name
      items {
        description
        itemId
        name
      }
      markets {
        location
        marketId
        name
      }
    }
    salesRep {
      resourceId
      salesRepId
      resource {
        name
        resourceId
      }
    }
    buyers {
      buyerId
      name
    }
  }
}
```
### Respuesta:

```
{
  "data": {
    "getHeaders": [
      {
        "active": "Y",
        "buyerId": 1003,
        "headerId": 1,
        "name": "Header Name 1",
        "salesRepId": 102,
        "lines": {
          "creationDate": "2023-01-01",
          "headerId": 1,
          "itemId": 701,
          "lineId": 55001,
          "marketId": 2201,
          "name": "Line Name 1",
          "items": {
            "description": "gold",
            "itemId": 701,
            "name": "gold"
          },
          "markets": {
            "location": "Europe",
            "marketId": 2201,
            "name": "NotSo Wet Market"
          }
        },
        "salesRep": {
          "resourceId": 12,
          "salesRepId": 102,
          "resource": {
            "name": "Jaba Maba",
            "resourceId": 12
          }
        },
        "buyers": {
          "buyerId": 1003,
          "name": "Simon Sims"
        }
      },
      {
        "active": "Y",
        "buyerId": 1002,
        "headerId": 2,
        "name": "Header Name 2",
        "salesRepId": 105,
        "lines": {
          "creationDate": "2022-01-05",
          "headerId": 2,
          "itemId": 701,
          "lineId": 55003,
          "marketId": 2203,
          "name": "Line Name 3",
          "items": {
            "description": "gold",
            "itemId": 701,
            "name": "gold"
          },
          "markets": {
            "location": "Africa",
            "marketId": 2203,
            "name": "Rainy Days Market"
          }
        },
        "salesRep": {
          "resourceId": 15,
          "salesRepId": 105,
          "resource": {
            "name": "Viper Song",
            "resourceId": 15
          }
        },
        "buyers": {
          "buyerId": 1002,
          "name": "Bobby DropTable"
        }
      },
    ]
  }
}
```

## Mutación:

```
mutation MyMutation {
  updateHeader(header: {name: "Mutation Update", headerId: 6}) {
    name
    salesRepId
    buyerId
    active
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
