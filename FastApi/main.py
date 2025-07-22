from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from app.websocket.client import websocket_client
import asyncio
import logging
from typing import Dict, Any
from app.database.database import engine, Base
from app.graphql.schema import graphql_app
from app.routers import routers
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers existentes
app.include_router(graphql_app, prefix="/graphql")
app.include_router(routers.router)

@app.on_event("startup")
async def startup():
    # Inicializar la base de datos
    Base.metadata.create_all(bind=engine)
    
    # Configurar manejadores de eventos WebSocket
    websocket_client.on("connection_success", handle_connection_success)
    websocket_client.on("message", handle_websocket_message)
    
    # Iniciar la conexión WebSocket en segundo plano
    asyncio.create_task(connect_websocket())

async def handle_connection_success(data: Dict[str, Any]):
    """Maneja el evento de conexión exitosa."""
    logger.info(f"Conexión WebSocket exitosa. Client ID: {data.get('clientId')}")
    
    # Unirse a la sala por defecto
    if await websocket_client.join_room("default_room"):
        logger.info("Unido a la sala 'default_room'")
    else:
        logger.warning("No se pudo unir a la sala 'default_room'")

async def handle_websocket_message(data: Dict[str, Any]):
    """Maneja los mensajes recibidos del WebSocket."""
    logger.info(f"Mensaje recibido: {data}")

async def connect_websocket():
    """Mantiene la conexión WebSocket activa."""
    while True:
        try:
            if not websocket_client.connected:
                await websocket_client.connect()
                logger.info("Cliente WebSocket conectado exitosamente")
            
            # Esperar un tiempo antes de verificar la conexión nuevamente
            await asyncio.sleep(10)
            
        except Exception as e:
            logger.error(f"Error en la conexión WebSocket: {e}")
            websocket_client.connected = False
            await asyncio.sleep(5)  # Esperar 5 segundos antes de reintentar

@app.on_event("shutdown")
async def shutdown():
    await websocket_client.close()
    engine.dispose()
    logger.info("Application shutdown complete")

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
            {"message": "Hello from FastAPI", "timestamp": str(datetime.utcnow())}
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