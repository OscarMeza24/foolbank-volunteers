import asyncio
import socketio

sio = socketio.AsyncClient()

async def main():
    try:
        await sio.connect('http://localhost:3001')
        print("Conectado al servidor Socket.IO")
        
        # Enviar un mensaje de prueba
        await sio.emit('test', {'message': 'Hola desde el cliente de prueba'})
        
        # Mantener la conexión abierta
        while True:
            await asyncio.sleep(1)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await sio.disconnect()

if __name__ == "__main__":
    asyncio.run(main())