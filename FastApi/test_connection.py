import asyncio
import websockets
import json

async def test_connection():
    uri = "ws://localhost:3001/ws"
    try:
        async with websockets.connect(uri) as websocket:
            print("Conectado al servidor WebSocket")
            message = {"event": "test", "data": {"message": "Hola desde prueba manual"}}
            await websocket.send(json.dumps(message))
            print("Mensaje enviado, esperando respuesta...")
            response = await websocket.recv()
            print(f"Respuesta recibida: {response}")
    except Exception as e:
        print(f"Error: {e}")

asyncio.get_event_loop().run_until_complete(test_connection())