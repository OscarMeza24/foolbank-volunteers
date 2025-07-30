# Módulo de Agente Autónomo para Análisis de Voluntarios

Este módulo implementa un agente autónomo que utiliza n8n para orquestar flujos de trabajo complejos para analizar voluntarios utilizando IA. El agente se integra con los demás microservicios del sistema para realizar análisis profundos de los voluntarios y generar recomendaciones personalizadas.

## 🚀 Características Principales

- **Análisis Automatizado**: Procesamiento automático de información de voluntarios
- **Integración con IA**: Utiliza modelos de lenguaje avanzados para análisis cualitativos
- **Flujos de Trabajo Personalizables**: Fácil de modificar y extender mediante n8n
- **Monitoreo en Tiempo Real**: Seguimiento del estado de los análisis
- **Historial Completo**: Almacenamiento de todos los análisis realizados

## 📋 Requisitos Previos

- Docker y Docker Compose (versión 2.0+)
- n8n (se instalará automáltcamente con Docker)
- Python 3.9 o superior
- API Key de OpenAI (o compatible con la API de OpenAI)
- Acceso a la base de datos de voluntarios

## 🛠️ Configuración del Entorno

### 1. Clonar el Repositorio

```bash
git clone https://github.com/OscarMeza24/foolbank-volunteers.git
cd foolbank-volunteers
```

### 2. Configuración de Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Configuración de la Aplicación
APP_ENV=development
DEBUG=True

# Base de Datos
DATABASE_URL=postgresql://user:password@localhost:5432/foolbank_volunteers
DATABASE_TEST_URL=sqlite:///./test.db

# Autenticación
SECRET_KEY=tu_clave_secreta_muy_larga_y_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24 horas

# OpenAI
OPENAI_API_KEY=tu_api_key_de_openai
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=2000

# n8n Configuration
N8N_HOST=localhost
N8N_PORT=5678
N8N_PROTOCOL=http
N8N_WEBHOOK_URL=http://localhost:5678/
N8N_WEBHOOK_PATH=/webhook/volunteer-analysis
N8N_TIMEOUT=30.0
N8N_RETRIES=3

# URL de la API de Voluntarios
VOLUNTEER_API_URL=http://localhost:8000/api/v1/volunteers
```

### 3. Iniciar los Servicios con Docker

El proyecto incluye un archivo `docker-compose.yml` que configura todos los servicios necesarios:

```bash
# Iniciar todos los servicios en segundo plano
docker-compose up -d

# Ver los logs de los servicios
docker-compose logs -f

# Detener los servicios
docker-compose down
```

### 4. Configuración de n8n

1. Acceder a la interfaz web de n8n en [http://localhost:5678](http://localhost:5678)
2. Importar el flujo desde `n8n_flows/volunteer_analysis_flow.json`
3. Configurar las credenciales de la API de OpenAI en el nodo correspondiente
4. Asegurarse de que el webhook esté correctamente configurado para recibir actualizaciones

### 5. Migraciones de Base de Datos

Asegúrate de ejecutar las migraciones de la base de datos:

```bash
alembic upgrade head
```

## 🚀 Uso de la API del Agente

### Autenticación

Todas las rutas requieren autenticación mediante JWT. Incluye el token en el header `Authorization`:

```
Authorization: Bearer tu_token_jwt_aquí
```

### 1. Iniciar un Análisis de Voluntario

**Endpoint:** `POST /api/v1/agent/analyze-volunteer`

Inicia un análisis asíncrono de un voluntario. Devuelve inmediatamente con un ID de análisis.

**Parámetros de la solicitud:**

| Parámetro      | Tipo    | Requerido | Descripción                                      |
|----------------|---------|-----------|--------------------------------------------------|
| voluntario_id  | integer | Sí        | ID del voluntario a analizar                     |
| parametros     | object  | No        | Parámetros adicionales para el análisis          |

**Estructura de `parametros`:**

| Campo                 | Tipo    | Requerido | Valor por defecto | Descripción                                      |
|-----------------------|---------|-----------|-------------------|--------------------------------------------------|
| incluir_historico     | boolean | No        | true             | Incluir historial previo del voluntario          |
| incluir_recomendaciones| boolean| No        | true             | Generar recomendaciones personalizadas           |
| idioma               | string  | No        | "es"             | Idioma para el análisis ("es" o "en")           |
| profundidad_analisis  | string  | No        | "medio"          | Nivel de profundidad ("básico", "medio", "avanzado") |

**Ejemplo de solicitud:**

```bash
curl -X POST "http://localhost:8000/api/v1/agent/analyze-volunteer" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer tu_token_jwt" \
  -d '{
    "voluntario_id": 1,
    "parametros": {
      "incluir_historico": true,
      "incluir_recomendaciones": true,
      "idioma": "es",
      "profundidad_analisis": "avanzado"
    }
  }'
```

**Respuesta exitosa (202 Accepted):**

```json
{
  "analysis_id": 42,
  "status": "pending",
  "message": "Análisis iniciado correctamente",
  "links": [
    {
      "rel": "status",
      "href": "/api/v1/agent/analysis/42",
      "method": "GET"
    }
  ]
}
```

### 2. Consultar el Estado de un Análisis

**Endpoint:** `GET /api/v1/agent/analysis/{analysis_id}`

Obtiene el estado actual de un análisis específico.

**Parámetros de la ruta:**

| Parámetro    | Tipo    | Requerido | Descripción                     |
|--------------|---------|-----------|---------------------------------|
| analysis_id  | integer | Sí        | ID del análisis a consultar     |

**Ejemplo de solicitud:**

```bash
curl -H "Authorization: Bearer tu_token_jwt" \
  "http://localhost:8000/api/v1/agent/analysis/42"
```

**Respuesta exitosa (200 OK):**

```json
{
  "analysis_id": 42,
  "voluntario_id": 1,
  "status": "completed",
  "progress": 100,
  "started_at": "2023-11-15T10:30:00Z",
  "completed_at": "2023-11-15T10:32:15Z",
  "result": {
    "resumen": "El voluntario muestra un excelente desempeño...",
    "puntos_fuertes": ["Liderazgo", "Trabajo en equipo"],
    "areas_mejora": ["Gestión del tiempo"],
    "recomendaciones": ["Asignar a proyectos de liderazgo"]
  },
  "metadata": {
    "model_used": "gpt-4-turbo-preview",
    "tokens_used": 1450,
    "processing_time_seconds": 135
  }
}
```

### 3. Listar Análisis de un Voluntario

**Endpoint:** `GET /api/v1/agent/volunteer/{voluntario_id}/analyses`

Obtiene todos los análisis realizados para un voluntario específico.

**Parámetros de consulta:**

| Parámetro | Tipo    | Requerido | Valor por defecto | Descripción                     |
|-----------|---------|-----------|-------------------|---------------------------------|
| limit     | integer | No        | 10                | Número máximo de resultados     |
| offset    | integer | No        | 0                 | Desplazamiento para paginación  |
| status    | string  | No        | -                 | Filtrar por estado (opcional)   |

**Ejemplo de solicitud:**

```bash
curl -H "Authorization: Bearer tu_token_jwt" \
  "http://localhost:8000/api/v1/agent/volunteer/1/analyses?limit=5&offset=0"
```

**Respuesta exitosa (200 OK):**

```json
{
  "items": [
    {
      "analysis_id": 42,
      "voluntario_id": 1,
      "status": "completed",
      "started_at": "2023-11-15T10:30:00Z",
      "completed_at": "2023-11-15T10:32:15Z"
    },
    {
      "analysis_id": 35,
      "voluntario_id": 1,
      "status": "completed",
      "started_at": "2023-11-10T14:20:00Z",
      "completed_at": "2023-11-10T14:22:30Z"
    }
  ],
  "total": 2,
  "limit": 5,
  "offset": 0
}
```

## 🏗️ Estructura del Proyecto

```
foolbank-volunteers/
├── FastApi/
│   ├── app/
│   │   ├── agent_flow/               # Módulo del agente autónomo
│   │   │   ├── __init__.py
│   │   │   ├── volunteer_analyzer.py # Lógica principal del analizador
│   │   │   ├── n8n_integration.py    # Integración con n8n
│   │   │   └── models.py             # Modelos de datos
│   │   │
│   │   └── api/
│   │       └── endpoints/
│   │           └── agent.py          # Endpoints de la API
│   │
│   └── n8n_flows/
│       └── volunteer_analysis_flow.json  # Flujo de n8n
│
└── docs/
    └── agent_workflow.md              # Documentación detallada del flujo
```

## 🔄 Flujo de Trabajo del Agente

El agente sigue un flujo de trabajo bien definido para procesar los análisis de voluntarios:

1. **Activación**
   - El cliente realiza una petición POST a `/api/v1/agent/analyze-volunteer`
   - Se valida la autenticación y los parámetros de entrada

2. **Registro Inicial**
   - Se crea un registro en la base de datos con estado `pending`
   - Se devuelve una respuesta inmediata con el ID del análisis

3. **Procesamiento Asíncrono**
   - El agente inicia un proceso en segundo plano
   - Se actualiza el estado a `processing`
   - Se recopilan datos del voluntario desde el microservicio correspondiente

4. **Análisis con IA**
   - Los datos se envían al flujo de n8n
   - n8n orquesta el proceso de análisis utilizando la API de OpenAI
   - Se generan recomendaciones personalizadas

5. **Almacenamiento de Resultados**
   - Los resultados se guardan en la base de datos
   - El estado se actualiza a `completed`
   - Se registran métricas de ejecución

6. **Notificación (Opcional)**
   - Se puede configurar una notificación vía email o WebSocket
   - El cliente puede consultar los resultados en cualquier momento

## 📊 Estados del Análisis

| Estado      | Descripción                                      |
|-------------|--------------------------------------------------|
| pending     | Análisis creado, pendiente de procesamiento     |
| processing | En proceso de análisis                          |
| completed  | Análisis completado con éxito                   |
| failed     | Error durante el procesamiento                  |
| cancelled  | Análisis cancelado por el usuario               |

## 🔒 Seguridad

- **Autenticación**: Todos los endpoints requieren autenticación JWT
- **Autorización**: Se verifican los permisos del usuario para acceder a los recursos
- **Validación de entrada**: Se validan todos los parámetros de entrada
- **Registro de auditoría**: Se registran todas las acciones importantes

## 🧪 Pruebas

El módulo incluye pruebas unitarias y de integración. Para ejecutarlas:

```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Ejecutar pruebas
pytest tests/agent_flow/

# Generar informe de cobertura
pytest --cov=app.agent_flow tests/agent_flow/
```

## 🐛 Solución de Problemas

### El análisis no se inicia
- Verifica que n8n esté en ejecución y accesible
- Comprueba los logs de la aplicación en busca de errores
- Asegúrate de que la API key de OpenAI sea válida

### Error 401 No autorizado
- Verifica que el token JWT sea válido y no haya expirado
- Asegúrate de incluir el token en el header `Authorization`

### El análisis tarda demasiado
- Revisa el estado de los servicios de n8n y OpenAI
- Verifica la carga del servidor
- Considera reducir la profundidad del análisis para análisis más rápidos

## 📝 Licencia

Este proyecto está licenciado bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, lee las [pautas de contribución](CONTRIBUTING.md) antes de enviar un pull request.

## 📞 Soporte

Para soporte, por favor abre un issue en el repositorio o contacta al equipo de desarrollo en soporte@foolbank.org.
3. **Recopilación de Datos**: Se obtienen los datos del voluntario y su historial de eventos
4. **Procesamiento con IA**: Se envía la información a OpenAI para generar un análisis
5. **Almacenamiento**: Se guardan los resultados en la base de datos
6. **Notificación**: Se notifica al usuario sobre la finalización del análisis

## Personalización

Puedes modificar el flujo de n8n para adaptarlo a tus necesidades:
- Agregar más fuentes de datos
- Modificar el prompt de OpenAI
- Integrar con otros servicios

## Solución de Problemas

- **Error de conexión con n8n**: Verifica que el servicio esté en ejecución con `docker ps`
- **Error de autenticación**: Verifica las credenciales en el archivo `.env`
- **Error de OpenAI**: Verifica que la API key sea válida y tenga saldo suficiente

## Licencia

Este proyecto está bajo la licencia MIT.
