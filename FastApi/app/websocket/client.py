import asyncio
import json
import socketio
from typing import Dict, Any, Optional, Callable, Awaitable
import logging

logger = logging.getLogger(__name__)

class WebSocketClient:
    def __init__(self, uri: str = "http://localhost:4005"):
        self.uri = uri.rstrip('/')
        self.sio = socketio.AsyncClient()
        self.connected = False
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5
        self.reconnect_delay = 1  # segundos
        self._message_handlers = {}  # Inicializar el diccionario de manejadores
        
        # Configurar manejadores de eventos
        @self.sio.event
        async def connect():
            self.connected = True
            self.reconnect_attempts = 0
            logger.info("Conexión WebSocket establecida")
            
        @self.sio.event
        async def disconnect():
            self.connected = False
            logger.warning("Desconectado del servidor WebSocket")
            
        @self.sio.event
        async def message(data):
            logger.debug(f"Mensaje recibido: {data}")
            await self._handle_message(data)

    async def connect(self, required: bool = False):
        """
        Establece la conexión con el servidor Socket.IO.
        
        Args:
            required: Si es True, lanza una excepción si no se puede conectar.
                     Si es False, solo registra un mensaje de advertencia.
        """
        if self.connected:
            logger.info("Ya hay una conexión activa")
            return True
            
        try:
            await self._attempt_connection()
            return True
        except Exception as e:
            if required:
                raise
            logger.warning(f"No se pudo conectar al WebSocket: {str(e)}")
            logger.warning("La aplicación continuará sin conexión WebSocket")
            return False
        
    async def _attempt_connection(self):
        """Intenta establecer la conexión con el servidor Socket.IO."""
        while self.reconnect_attempts < self.max_reconnect_attempts:
            try:
                logger.info(f"Intentando conectar a Socket.IO en {self.uri} (intento {self.reconnect_attempts + 1}/{self.max_reconnect_attempts})")
                
                await self.sio.connect(
                    self.uri,
                    socketio_path='/socket.io',  
                    namespaces=['/'],
                    transports=['websocket'],
                    wait_timeout=10
                )
                
                logger.info("Conexión WebSocket establecida exitosamente")
                self.connected = True
                self.reconnect_attempts = 0
                return
                
            except Exception as e:
                self.reconnect_attempts += 1
                logger.error(f"Error al conectar a Socket.IO (intento {self.reconnect_attempts}/{self.max_reconnect_attempts}): {str(e)}")
                
                if self.reconnect_attempts >= self.max_reconnect_attempts:
                    logger.error("Se agotaron los intentos de conexión")
                    raise ConnectionError("No se pudo establecer la conexión con el servidor WebSocket")
                
                # Esperar antes de reintentar
                await asyncio.sleep(self.reconnect_delay)
                self.reconnect_delay = min(self.reconnect_delay * 2, 30)  

    def on(self, event: str, handler: Callable[[Any], Awaitable[None]]):
        """Registra un manejador para un evento específico."""
        if event not in self._message_handlers:
            self._message_handlers[event] = []
            
            # Registrar el manejador en Socket.IO
            @self.sio.on(event)
            async def handle_event(data):
                if event in self._message_handlers:  # Verificar que el evento aún tenga manejadores
                    for h in self._message_handlers[event]:
                        try:
                            if asyncio.iscoroutinefunction(h):
                                await h(data)
                            else:
                                h(data)
                        except Exception as e:
                            logger.error(f"Error en el manejador para {event}: {e}")
                
        self._message_handlers[event].append(handler)
        return self

    async def _handle_message(self, data):
        """Maneja los mensajes entrantes y los redirige a los manejadores registrados."""
        logger.debug(f"Manejando mensaje: {data}")
        
        # Si el mensaje es un diccionario con 'event' y 'data', lo procesamos
        if isinstance(data, dict):
            # Si es una respuesta del servidor con 'status', solo la registramos
            if 'status' in data and 'event' in data:
                logger.info(f"Respuesta del servidor: {data}")
                return
                
            # Si tiene 'event' y 'data', lo manejamos según el evento
            if 'event' in data and 'data' in data:
                event = data['event']
                if event in self._message_handlers:
                    for handler in self._message_handlers[event]:
                        try:
                            await handler(data['data'])
                        except Exception as e:
                            logger.error(f"Error en el manejador para {event}: {e}")
    

    async def _reconnect(self):
        """Intenta reconectarse al servidor Socket.IO."""
        self.connected = False
        if self.sio.connected:
            try:
                await self.sio.disconnect()
            except Exception as e:
                logger.error(f"Error al cerrar la conexión: {e}")
            
        await asyncio.sleep(self.reconnect_delay)
        try:
            await self._attempt_connection()
        except Exception as e:
            logger.error(f"Error al reconectar: {e}")
            
    async def send_json(self, event: str, data: Dict[str, Any]) -> bool:
        """Envía un mensaje JSON al servidor."""
        if not self.connected:
            logger.warning("No hay conexión activa")
            return False
            
        try:
            await self.sio.emit(event, data)
            return True
        except Exception as e:
            logger.error(f"Error al enviar mensaje: {e}")
            self.connected = False
            return False

    async def send_message(self, room: str, event: str, data: dict) -> bool:
        """Envía un mensaje a una sala específica."""
        try:
            if not self.connected:
                logger.warning("No hay conexión activa. Intentando reconectar...")
                try:
                    await self.connect()
                except Exception as e:
                    logger.error(f"No se pudo establecer la conexión: {e}")
                    return False

            # Formato del mensaje que espera el servidor
            message = {
                'event': event,
                'data': data,
                'room': room
            }
            
            # Enviamos el mensaje al evento 'message' que está configurado en el servidor
            await self.sio.emit('message', message)
            logger.info(f"Mensaje enviado a la sala {room}: {message}")
            return True
            
        except Exception as e:
            logger.error(f"Error al enviar mensaje: {e}")
            self.connected = False
            return False

    async def join_room(self, room: str) -> bool:
        """Se une a una sala específica."""
        if not self.connected:
            return False
        try:
            await self.sio.emit('join_room', {'room': room})
            return True
        except Exception as e:
            logger.error(f"Error al unirse a la sala {room}: {e}")
            return False

    
    async def leave_room(self, room: str) -> bool:
        """Abandona una sala específica."""
        if not self.connected:
            return False
        try:
            await self.sio.emit('leave_room', {'room': room})
            return True
        except Exception as e:
            logger.error(f"Error al salir de la sala {room}: {e}")
            return False

    async def close(self):
        """Cierra la conexión Socket.IO."""
        if self.connected:
            try:
                await self.sio.disconnect()
                logger.info("Conexión cerrada correctamente")
            except Exception as e:
                logger.error(f"Error al cerrar la conexión: {e}")
            finally:
                self.connected = False
                self.reconnect_attempts = 0

# Instancia global del cliente WebSocket
websocket_client = WebSocketClient()