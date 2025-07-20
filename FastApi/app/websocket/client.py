import asyncio
import json
import websockets
from typing import Dict, Any

class WebSocketClient:
    def __init__(self, uri: str = "ws://localhost:3001/"):
        self.uri = uri
        self.connection = None

    async def connect(self):
        try:
            self.connection = await websockets.connect(self.uri)
            print(f"Conectado a WebSocket en {self.uri}")
            return self
        except Exception as e:
            print(f"Error al conectar a WebSocket: {e}")
            raise

    async def send_message(self, event: str, data: Dict[str, Any]):
        if self.connection:
            message = json.dumps({"event": event, "data": data})
            print(f"Enviando mensaje: {message}")
            await self.connection.send(message)

    async def close(self):
        if self.connection:
            await self.connection.close()
            print("Conexión WebSocket cerrada")

websocket_client = WebSocketClient()