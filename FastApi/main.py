from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from app.websocket.client import websocket_client
import asyncio
import sqlalchemy
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
    Base.metadata.create_all(bind=engine)
    try:
        await websocket_client.connect()
        logger.info("WebSocket client connected successfully")
    except Exception as e:
        logger.error(f"Failed to connect WebSocket: {e}")

@app.on_event("shutdown")
async def shutdown():
    await websocket_client.close()
    engine.dispose()
    logger.info("Application shutdown complete")

@app.get("/test-ws")
async def test_websocket():
    try:
        await websocket_client.send_message("test", {"message": "Hello from FastAPI"})
        return {
            "status": "success",
            "message": "Mensaje enviado correctamente al WebSocket",
            "data": {
                "event": "test",
                "timestamp": datetime.now().isoformat()
            }
        }
    except Exception as e:
        logger.error(f"Error sending WebSocket message: {e}")
        return {
            "status": "error",
            "message": "Error al enviar el mensaje al WebSocket",
            "error": str(e)
        }