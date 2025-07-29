interface WebSocketConfig {
  path: string;
  cors: {
    origin: string | string[];
    methods: string[];
    credentials: boolean;
  };
}

export interface AppConfig {
  port: number;
  host: string;
  environment: string;
  websocket: WebSocketConfig;
}

export default (): AppConfig => ({
  port: process.env.PORT ? parseInt(process.env.PORT, 10) : 4005,
  host: process.env.HOST || '0.0.0.0',
  environment: process.env.NODE_ENV || 'development',
  websocket: {
    path: '/ws',
    cors: {
      origin: process.env.WS_CORS_ORIGIN?.split(',') || '*',
      methods: ['GET', 'POST'],
      credentials: true,
    },
  },
});
