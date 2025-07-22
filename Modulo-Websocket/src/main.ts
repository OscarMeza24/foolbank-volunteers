import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { Logger } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';

async function bootstrap() {
  const app = await NestFactory.create(AppModule, {
    logger: ['error', 'warn', 'log', 'debug', 'verbose'],
    cors: true,
  });

  const configService = app.get(ConfigService);

  // Obtener configuración con valores por defecto
  const port = configService.get<number>('port', 3000);
  const host = configService.get<string>('host', '0.0.0.0');
  const environment = configService.get<string>('environment', 'development');
  const wsPath = configService.get<string>('websocket.path', '/ws');

  // Configuración de CORS con valores por defecto
  const corsConfig = {
    origin: configService.get<string | string[]>('websocket.cors.origin', '*'),
    methods: configService.get<string[]>('websocket.cors.methods', [
      'GET',
      'POST',
    ]),
    credentials: configService.get<boolean>('websocket.cors.credentials', true),
  };

  // Configuración global de prefijos
  app.setGlobalPrefix('api');

  // Habilitar CORS
  app.enableCors(corsConfig);

  // Mostrar configuración cargada
  const logger = new Logger('Bootstrap');
  logger.log('Configuración cargada:');
  logger.log(`- Puerto: ${port}`);
  logger.log(`- Host: ${host}`);
  logger.log(`- Entorno: ${environment}`);
  logger.log(`- Ruta WebSocket: ${wsPath}`);
  logger.log(`- CORS: ${JSON.stringify(corsConfig)}`);

  // Iniciar el servidor
  await app.listen(port, host);
  logger.log(`Aplicación iniciada en ${await app.getUrl()}`);

  logger.log(`Modo: ${environment}`);
  logger.log(`Servidor WebSocket ejecutándose en: ${host}:${port}`);
  logger.log(`Ruta de WebSocket: ws://${host}:${port}${wsPath}`);
}

bootstrap().catch((error: Error) => {
  const logger = new Logger('Bootstrap');
  logger.error('Error al iniciar la aplicación:', error);
  process.exit(1);
});
