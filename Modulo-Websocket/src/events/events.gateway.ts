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

type WebSocketEvent =
  | 'broadcast'
  | 'private'
  | 'message'
  | 'notification'
  | string; // This allows other strings while maintaining autocompletion

interface MessagePayload<T = BaseMessageData> {
  event: WebSocketEvent;
  data: T;
}

interface SocketResponse<T = unknown> {
  status: 'received' | 'success' | 'error';
  event: WebSocketEvent;
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
  private logger: Logger = new Logger('EventsGateway');
  private clients: Map<string, Socket> = new Map();

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
  handleMessage(client: Socket, payload: MessagePayload): void {
    const { event, data } = payload;
    this.logger.log(
      `Mensaje recibido de ${client.id}: ${JSON.stringify(payload)}`,
    );

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
    event: WebSocketEvent,
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
