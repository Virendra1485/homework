import asyncio
import websockets


async def test_websocket_connection():
    uri = "ws://127.0.0.1:8000/ws/socket-server/"  # Replace with your WebSocket URL

    try:
        async with websockets.connect(uri) as websocket:
            # Send a test message to the server
            message = "Hello, WebSocket Server!"
            try:
                await websocket.send(message)
            except Exception as e:
                print(e)
            print(f"Sent: {message}")

            # Receive and print the response from the server
            response = await websocket.recv()
            print(f"Received: {response}")
    except Exception as e:
        print(e, "---------------")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(test_websocket_connection())
