import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { WebSocketGateway } from '@nestjs/websockets';
import { EventsGateway } from './events/events.gateway';
import configuration from './config/configuration';

@WebSocketGateway({
  cors: {
    origin: '*',
    methods: ['GET', 'POST'],
    credentials: true,
  },
  path: '/socket.io/',
})
@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      load: [configuration],
    }),
  ],
  controllers: [],
  providers: [EventsGateway],
})
export class AppModule {}
