# Módulo de Agente Autónomo para Análisis de Voluntarios

Este módulo implementa un agente autónomo que analiza el desempeño de los voluntarios utilizando inteligencia artificial. El agente puede ser activado mediante una API REST y ejecuta un flujo de trabajo asíncrono para generar análisis detallados.

## Características

- **Análisis Automático**: Evalúa el desempeño de los voluntarios basado en su participación en eventos.
- **Integración con LLM**: Utiliza modelos de lenguaje avanzados para generar recomendaciones personalizadas.
- **Procesamiento Asíncrono**: Las tareas de análisis se ejecutan en segundo plano sin bloquear la API.
- **Persistencia de Resultados**: Los análisis generados se almacenan en la base de datos para su posterior consulta.
- **Monitoreo de Estado**: Permite consultar el estado de los análisis en cualquier momento.

## Estructura del Módulo

```
agent_flow/
├── __init__.py
├── volunteer_analyzer.py  # Lógica principal del analizador
└── README.md             # Este archivo

schemas/agent/
├── __init__.py
└── volunteer_analysis.py  # Esquemas Pydantic para el análisis

models/
└── agent_models.py       # Modelos de base de datos para análisis

api/endpoints/agent/
└── volunteer_analysis.py # Endpoints de la API para el agente
```

## Endpoints de la API

### 1. Iniciar Análisis de Voluntario

**Endpoint:** `POST /api/v1/agent/analyze-volunteer`

Inicia un análisis asíncrono para un voluntario específico.

**Cuerpo de la solicitud (JSON):**
```json
{
  "voluntario_id": 1,
  "incluir_historico": true,
  "incluir_recomendaciones": true,
  "idioma": "es"
}
```

**Respuesta Exitosa (202 Accepted):**
```json
{
  "id": 1,
  "voluntario_id": 1,
  "estado": "pending",
  "parametros": {
    "incluir_historico": true,
    "incluir_recomendaciones": true,
    "idioma": "es"
  },
  "fecha_creacion": "2023-07-29T17:53:00.000Z"
}
```

### 2. Consultar Estado de Análisis

**Endpoint:** `GET /api/v1/agent/analysis/{analysis_id}`

Obtiene el estado actual de un análisis específico.

**Respuesta Exitosa (200 OK):**
```json
{
  "id": 1,
  "voluntario_id": 1,
  "estado": "completed",
  "parametros": {
    "incluir_historico": true,
    "incluir_recomendaciones": true,
    "idioma": "es"
  },
  "resultado": {
    "voluntario_id": 1,
    "resumen": "Voluntario altamente comprometido con excelentes habilidades de liderazgo.",
    "fortalezas": [
      "Excelente comunicación con los participantes",
      "Liderazgo demostrado en múltiples eventos"
    ],
    "areas_mejora": [
      "Podría mejorar en la documentación post-evento"
    ],
    "recomendaciones": [
      "Asignar como líder de equipo en eventos futuros"
    ],
    "eventos_participados": 5,
    "calificacion_promedio": 4.5,
    "ultima_participacion": "2023-07-15"
  },
  "fecha_creacion": "2023-07-29T17:53:00.000Z",
  "fecha_actualizacion": "2023-07-29T17:53:30.000Z"
}
```

### 3. Obtener Historial de Análisis de un Voluntario

**Endpoint:** `GET /api/v1/agent/volunteer/{voluntario_id}/analyses`

Obtiene todos los análisis realizados para un voluntario específico.

**Parámetros de Consulta:**
- `skip` (opcional): Número de registros a omitir (paginación)
- `limit` (opcional): Número máximo de registros a devolver (por defecto: 10)

**Respuesta Exitosa (200 OK):**
```json
[
  {
    "id": 1,
    "voluntario_id": 1,
    "estado": "completed",
    "fecha_creacion": "2023-07-29T17:53:00.000Z",
    "fecha_actualizacion": "2023-07-29T17:53:30.000Z"
  },
  ...
]
```

## Configuración

El módulo requiere las siguientes variables de entorno:

```env
# Configuración de OpenAI
OPENAI_API_KEY=tu_api_key_aqui
OPENAI_MODEL=gpt-3.5-turbo

# URL base de la API interna
INTERNAL_API_BASE_URL=http://localhost:8000/api/v1

# Nivel de registro (debug, info, warning, error, critical)
LOG_LEVEL=info
```

## Flujo de Trabajo del Agente

1. **Activación**: Un cliente llama al endpoint `/api/v1/agent/analyze-volunteer`
2. **Inicio del Proceso**: Se crea un registro en la base de datos con estado "pending"
3. **Procesamiento Asíncrono**: Un worker en segundo plano inicia el análisis
4. **Recopilación de Datos**: El agente recopila información del voluntario y su historial
5. **Análisis con LLM**: Los datos se envían a un modelo de lenguaje para su procesamiento
6. **Almacenamiento**: Los resultados se guardan en la base de datos
7. **Notificación**: Se puede configurar una notificación cuando el análisis esté completo

## Integración con n8n (Opcional)

El módulo puede integrarse con n8n para flujos de trabajo más complejos. Para ello, configura un webhook en n8n que escuche el evento de finalización de análisis.

## Próximos Pasos

- [ ] Implementar integración con n8n para flujos personalizados
- [ ] Añadir más métricas de análisis
- [ ] Implementar notificaciones por correo electrónico
- [ ] Añadir soporte para múltiples idiomas
- [ ] Implementar caché para análisis recientes
