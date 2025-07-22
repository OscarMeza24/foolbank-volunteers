import asyncio
import json
import websockets
from typing import Dict, Any, Optional, Callable, Awaitable
import logging
import time

logger = logging.getLogger(__name__)

class WebSocketClient:
    def __init__(self, uri: str = "ws://localhost:3000"):
        # Asegurarse de que la URI no termine con /ws ya que se añadirá después
        self.uri = uri.rstrip('/')
        self.connection: Optional[websockets.WebSocketClientProtocol] = None
        self.connected = False
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5
        self.reconnect_delay = 2  # segundos
        self._message_handlers = {}
        self._running = False
        self._receive_task: Optional[asyncio.Task] = None

    async def connect(self):
        """Establece la conexión con el servidor WebSocket."""
        if self.connected and self.connection and not self.connection.closed:
            logger.info("Ya hay una conexión WebSocket activa")
            return self
            
        self.reconnect_attempts = 0
        await self._attempt_connection()
        self._running = True
        self._receive_task = asyncio.create_task(self._receive_messages())
        return self
        
    async def _attempt_connection(self):
        """Intenta establecer la conexión con el servidor WebSocket."""
        while self.reconnect_attempts < self.max_reconnect_attempts:
            try:
                logger.info(f"Intentando conectar a WebSocket en {self.uri} (intento {self.reconnect_attempts + 1}/{self.max_reconnect_attempts})")
                # Añadir el path /socket.io/ al URI para compatibilidad con Socket.IO
                socket_io_uri = f"{self.uri}/socket.io/?EIO=3&transport=websocket"
                
                # Configurar los headers necesarios para Socket.IO
                self.connection = await websockets.connect(
                    socket_io_uri,
                    ping_interval=25,
                    ping_timeout=60,
                    close_timeout=5,
                    extra_headers={
                        'Origin': 'http://localhost:3000/ws',
                        'Sec-WebSocket-Protocol': 'websocket',
                        'Upgrade': 'websocket',
                        'Connection': 'Upgrade'
                    },
                    max_size=10_000_000  # 10MB
                )
                self.connected = True
                self.reconnect_attempts = 0
                logger.info(f"Conectado exitosamente a WebSocket en {self.uri}")
                return
            except Exception as e:
                self.reconnect_attempts += 1
                logger.error(f"Error al conectar a WebSocket (intento {self.reconnect_attempts}/{self.max_reconnect_attempts}): {str(e)}")
                if self.reconnect_attempts < self.max_reconnect_attempts:
                    await asyncio.sleep(self.reconnect_delay)
                else:
                    logger.error("Se agotaron los intentos de conexión")
                    self.connected = False
                    raise

    async def _receive_messages(self):
        """Escucha mensajes del servidor WebSocket."""
        while self._running:
            try:
                if not self.connected or not self.connection or self.connection.closed:
                    await asyncio.sleep(1)
                    continue
                    
                message = await self.connection.recv()
                self._handle_message(message)
                
            except websockets.exceptions.ConnectionClosed as e:
                logger.error(f"Conexión WebSocket cerrada: {e}")
                self.connected = False
                await self._reconnect()
                
            except Exception as e:
                logger.error(f"Error al recibir mensaje: {e}")
                self.connected = False
                await asyncio.sleep(1)

    async def _handle_message(self, message: str):
        """Procesa un mensaje recibido del servidor."""
        try:
            data = json.loads(message)
            event = data.get('event')
            
            if event and event in self._message_handlers:
                for handler in self._message_handlers[event]:
                    task = asyncio.create_task(handler(data.get('data')))
                    await task
                    
        except json.JSONDecodeError:
            logger.warning(f"Mensaje no es un JSON válido: {message}")
        except Exception as e:
            logger.error(f"Error al procesar mensaje: {e}")

    def on(self, event: str, handler: Callable[[Any], Awaitable[None]]):
        """Registra un manejador para un evento específico."""
        if event not in self._message_handlers:
            self._message_handlers[event] = []
        self._message_handlers[event].append(handler)
        return self

    async def _reconnect(self):
        """Intenta reconectarse al servidor WebSocket."""
        self.connected = False
        if self.connection:
            try:
                await self.connection.close()
            except Exception as e:
                logger.error(f"Error al cerrar la conexión WebSocket: {e}")
            
        await asyncio.sleep(self.reconnect_delay)
        try:
            await self._attempt_connection()
        except Exception as e:
            logger.error(f"Error al reconectar: {e}")
            
    async def send_json(self, data: Dict[str, Any]) -> bool:
        """Envía un mensaje JSON al servidor."""
        if not self.connected or not self.connection or self.connection.closed:
            logger.warning("No hay conexión WebSocket activa")
            return False
            
        try:
            await self.connection.send(json.dumps(data))
            return True
        except Exception as e:
            logger.error(f"Error al enviar mensaje: {e}")
            self.connected = False
            return False

    async def send_message(self, room: str, event: str, data: Dict[str, Any]) -> bool:
        """Envía un mensaje a una sala específica."""
        if not self.connection or self.connection.closed or not self.connected:
            logger.warning("No hay conexión WebSocket activa. Intentando reconectar...")
            try:
                await self.connect()
                # Esperar un momento después de reconectar
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"Error al reconectar: {e}")
                return False
                
        # Si después de reconectar aún no hay conexión, salir
        if not self.connection or self.connection.closed or not self.connected:
            logger.error("No se pudo establecer la conexión WebSocket")
            return False

        try:
            message = json.dumps({
                "room": room,
                "event": event,
                "data": data
            })
            logger.debug(f"Enviando mensaje a la sala '{room}': {message}")
            await self.connection.send(message)
            return True
        except Exception as e:
            logger.error(f"Error al enviar mensaje: {e}")
            self.connected = False
            return False

    async def join_room(self, room: str) -> bool:
        """Se une a una sala específica."""
        return await self.send_message(room, "join_room", {"room": room})

    async def leave_room(self, room: str) -> bool:
        """Abandona una sala específica."""
        return await self.send_message(room, "leave_room", {"room": room})

    async def close(self):
        """Cierra la conexión WebSocket."""
        if self.connection and not self.connection.closed:
            try:
                await self.connection.close()
                logger.info("Conexión WebSocket cerrada correctamente")
            except Exception as e:
                logger.error(f"Error al cerrar la conexión WebSocket: {e}")
            finally:
                self.connected = False
                self.connection = None
                self.reconnect_attempts = 0

# Instancia global del cliente WebSocket
websocket_client = WebSocketClient()