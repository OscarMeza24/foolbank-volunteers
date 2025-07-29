import {
  SubscribeMessage,
  WebSocketGateway,
  WebSocketServer,
  OnGatewayConnection,
  OnGatewayDisconnect,
  OnGatewayInit,
} from '@nestjs/websockets';
import { Logger } from '@nestjs/common';
import { Server, Socket } from 'socket.io';

interface BaseMessageData {
  message: string;
  [key: string]: unknown;
}

interface PrivateMessageData extends BaseMessageData {
  to: string;
  message: string;
}

interface BroadcastMessageData extends BaseMessageData {
  message: string;
}

interface MessagePayload<T = BaseMessageData> {
  event: string;
  data: T;
  room?: string;
}

interface SocketResponse<T = unknown> {
  status: 'received' | 'success' | 'error';
  event: string;
  data: T;
  timestamp: string;
}

@WebSocketGateway({
  namespace: '/',
  path: '/socket.io/',
})
export class EventsGateway
  implements OnGatewayInit, OnGatewayConnection, OnGatewayDisconnect
{
  @WebSocketServer() server: Server;
  private readonly logger: Logger = new Logger('EventsGateway');
  private readonly clients: Map<string, Socket> = new Map();

  afterInit(server: Server) {
    this.server = server;
    this.logger.log('WebSocket Gateway inicializado');
  }

  handleConnection(client: Socket) {
    const clientId = client.id;
    this.clients.set(clientId, client);
    this.logger.log(`Cliente conectado: ${clientId}`);
    // Enviar un mensaje de bienvenida
    client.emit('connection', {
      status: 'connected',
      clientId,
      timestamp: new Date().toISOString(),
    });

    // Notificar a otros clientes
    client.broadcast.emit('userConnected', { clientId });
  }

  handleDisconnect(client: Socket) {
    const clientId = client.id;
    this.clients.delete(clientId);
    this.logger.log(`Cliente desconectado: ${clientId}`);
    // Notificar a otros clientes
    client.broadcast.emit('userDisconnected', { clientId });
  }

  @SubscribeMessage('message')
  handleMessage(client: Socket, payload: any): void {
    this.logger.log(`Mensaje recibido de ${client.id}: ${JSON.stringify(payload)}`);

    // Manejar diferentes formatos de mensaje
    let event: string;
    let data: any;
    let room: string | undefined;

    // Formato 1: { event, data, room? }
    if ('event' in payload && 'data' in payload) {
        event = payload.event;
        data = payload.data;
        room = payload.room;
    }
    // Formato 2: { room, data: { event, data } }
    else if ('room' in payload && 'data' in payload && payload.data && typeof payload.data === 'object' && 'event' in payload.data) {
        room = payload.room;
        event = payload.data.event;
        data = payload.data.data || payload.data; // Asegurarse de manejar ambos formatos
    } else {
        // Formato no reconocido
        this.logger.error(`Formato de mensaje no reconocido: ${JSON.stringify(payload)}`);
        return;
    }

    // Unir a la sala si el evento es 'join'
    if (event === 'join' && data && data.room) {
      client.join(data.room);
      this.logger.log(`Cliente ${client.id} unido a la sala ${data.room}`);
      return;
    }

    // Manejar notificaciones
    if (event === 'notificacion') {
      // Si el mensaje incluye una sala, lo enviamos solo a esa sala
      if (room) {
        this.server.to(room).emit('notificacion', data);
      } else {
        // Si no hay sala, emitimos a todos
        this.server.emit('notificacion', data);
      }
    }

    // Si el evento es de inventario o solicitud, reenviarlo como 'notificacion'
    if (['nuevo-inventario', 'nueva-solicitude', 'organizacion-actualizada', 'organizacion-eliminada', 'inventario-actualizado','inventario-eliminado', 'solicitud-actualizada', 'solicitud-eliminada',
      'nuevo-donante', 'donante-eliminado', 'nuevo-receptor', 'receptor-eliminado'
    ].includes(event)) {
      const notificacion = {
        event,
        data,
        timestamp: new Date().toISOString()
      };
      if (room) {
        this.server.to(room).emit('notificacion', notificacion);
      } else {
        this.server.emit('notificacion', notificacion);
      }
      return;
    }

    // Manejar diferentes tipos de mensajes
    switch (event) {
      case 'broadcast': {
        const broadcastData = data as BroadcastMessageData;
        // Enviar a todos los clientes conectados
        this.server.emit('broadcast', {
          status: 'received',
          event,
          data: {
            from: client.id,
            message: broadcastData.message,
            timestamp: new Date().toISOString(),
          },
          timestamp: new Date().toISOString(),
        } as SocketResponse);
        break;
      }
      case 'private': {
        const privateData = data as PrivateMessageData;
        // Enviar a un cliente específico
        if (privateData.to && this.clients.has(privateData.to)) {
          this.server.to(privateData.to).emit('private', {
            status: 'received',
            event,
            data: {
              from: client.id,
              message: privateData.message,
              timestamp: new Date().toISOString(),
            },
            timestamp: new Date().toISOString(),
          } as SocketResponse);
        }
        break;
      }
      case 'nueva-organizacion': {
        this.server.emit('nueva-organizacion', {
          status: 'success',
          event: 'nueva-organizacion',
          data,
          timestamp: new Date().toISOString(),
        });
        break;
      }     
      default:
        // Respuesta por defecto
        client.emit('message', {
          status: 'received',
          event,
          data,
          timestamp: new Date().toISOString(),
        } as SocketResponse);
    }
  }
  

  // Método para enviar notificaciones a todos los clientes
  broadcastNotification(
    event: string,
    message: string,
    data: Record<string, unknown> = {},
  ) {
    this.server.emit('notification', {
      status: 'received',
      event,
      data,
      timestamp: new Date().toISOString(),
    });
  }

  // Método para obtener la lista de clientes conectados
  getConnectedClients(): string[] {
    return Array.from(this.clients.keys());
  }
}
