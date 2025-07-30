from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from app.websocket.client import websocket_client
import asyncio
import logging
import uvicorn
from typing import Dict, Any
from app.db import engine, Base, get_db, SessionLocal
from app.graphql.schema import graphql_app
from app.routers import routers
from app.auth.routes import router as auth_router
from app.models.agent_models import add_relationship_to_volunteers, AnalysisStatus, VolunteerAnalysis
from app.api.endpoints.agent import router as agent_router
from app.agent_flow.n8n_integration import n8n, startup_n8n_client, shutdown_n8n_client

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def connect_websocket():
    """Inicia la conexión WebSocket."""
    try:
        await websocket_client.connect()
        logger.info("Conectado al servidor WebSocket")
    except Exception as e:
        logger.error(f"Error al conectar al WebSocket: {e}")

app = FastAPI(title="FoolBank Volunteers API",
                description="API para la gestión de voluntarios de FoolBank",
                version="1.0.0")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers existentes
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(routers.router, prefix="/api", tags=["api"])
app.include_router(graphql_app, prefix="/graphql")
app.include_router(agent_router, prefix="/api/v1/agent", tags=["agent"])

async def notificacion_handler(data):
    print("Notificación recibida:", data)

@app.on_event("startup")
async def startup_event():
    """Evento que se ejecuta al iniciar la aplicación."""
    logger.info("Iniciando aplicación...")
    
    # Inicializar la base de datos
    Base.metadata.create_all(bind=engine)
    
    # Añadir relaciones al modelo Voluntarios
    add_relationship_to_volunteers()
    
    # Configurar manejadores de eventos WebSocket
    websocket_client.on("connection_success", handle_connection_success)
    websocket_client.on("message", handle_websocket_message)
    websocket_client.on('notificacion', notificacion_handler)
    
    # Iniciar cliente n8n
    await startup_n8n_client()
    
    # Intentar conectar al WebSocket (no es crítico si falla)
    try:
        connected = await websocket_client.connect(required=False)
        if connected:
            logger.info("Conexión WebSocket establecida exitosamente")
        
        # Suscribirse al evento 'nueva-organizacion'
        async def handle_nueva_organizacion(data):
            logger.info(f"Evento 'nueva-organizacion' recibido: {data}")
            # Aquí puedes agregar la lógica para manejar el evento
        
        websocket_client.on("nueva-organizacion", handle_nueva_organizacion)
        
        # Iniciar la conexión WebSocket en segundo plano
        task = asyncio.create_task(connect_websocket())
        return task
        
    except Exception as e:
        logger.warning(f"No se pudo conectar al WebSocket: {e}")
        logger.warning("La aplicación continuará sin funcionalidad de WebSocket")
        return None

async def handle_connection_success(data: Dict[str, Any]):
    """Maneja el evento de conexión exitosa."""
    logger.info(f"Conexión WebSocket exitosa. Client ID: {data.get('clientId')}")
    
    # Unirse a la sala por defecto
    if await websocket_client.join_room("default_room"):
        logger.info("Unido a la sala 'default_room'")
    else:
        logger.warning("No se pudo unir a la sala 'default_room'")

def handle_websocket_message(data: Dict[str, Any]):
    """Maneja los mensajes recibidos del WebSocket."""
    logger.info(f"Mensaje recibido: {data}")

async def connect_websocket():
    """Mantiene la conexión WebSocket activa."""
    while True:
        try:
            if not websocket_client.connected:
                connected = await websocket_client.connect(required=False)
                if connected:
                    logger.info("Cliente WebSocket conectado exitosamente")
                else:
                    logger.warning("No se pudo conectar al WebSocket, reintentando en 30 segundos...")
                    await asyncio.sleep(30)  # Esperar más tiempo antes de reintentar
                    continue
            
            # Esperar un tiempo antes de verificar la conexión nuevamente
            await asyncio.sleep(10)  # Verificar cada 10 segundos
            
        except asyncio.CancelledError:
            logger.info("Tarea de conexión WebSocket cancelada")
            break
        except Exception as e:
            logger.error(f"Error en la conexión WebSocket: {e}")
            logger.info("Reintentando en 30 segundos...")
            await asyncio.sleep(30)  # Esperar más tiempo antes de reintentar

@app.on_event("shutdown")
async def shutdown():
    """Evento que se ejecuta al cerrar la aplicación."""
    logger.info("Iniciando cierre ordenado de la aplicación...")
    
    # Cerrar la conexión WebSocket si está activa
    try:
        if hasattr(websocket_client, 'connected') and websocket_client.connected:
            await websocket_client.close()
            logger.info("Conexión WebSocket cerrada correctamente")
    except Exception as e:
        logger.error(f"Error al cerrar la conexión WebSocket: {e}")
    
    # Cerrar la conexión a la base de datos
    try:
        engine.dispose()
        logger.info("Conexión a la base de datos cerrada correctamente")
    except Exception as e:
        logger.error(f"Error al cerrar la conexión a la base de datos: {e}")
    
    # Cerrar cliente n8n
    try:
        await shutdown_n8n_client()
        logger.info("Cliente n8n cerrado correctamente")
    except Exception as e:
        logger.error(f"Error al cerrar el cliente n8n: {e}")
    
    logger.info("Aplicación cerrada correctamente")

@app.get("/test-ws")
async def test_websocket():
    """Endpoint de prueba para enviar un mensaje a través del WebSocket."""
    try:
        # Unirse a la sala de prueba
        joined = await websocket_client.join_room("test_room")
        if not joined:
            return {"status": "error", "message": "No se pudo unir a la sala"}
            
        # Enviar mensaje a la sala
        sent = await websocket_client.send_message(
            "test_room",
            "test_message",
            {"message": "Hello from FastAPI", "timestamp": str(datetime.now())}
        )
        
        if sent:
            return {
                "status": "success",
                "message": "Mensaje enviado correctamente al WebSocket",
                "data": {
                    "event": "test",
                    "timestamp": datetime.now().isoformat()
                }
            }
        else:
            return {
                "status": "error",
                "message": "Error al enviar el mensaje al WebSocket"
            }
    except Exception as e:
        logger.error(f"Error sending WebSocket message: {e}")
        return {
            "status": "error",
            "message": "Error al enviar el mensaje al WebSocket",
            "error": str(e)
        }