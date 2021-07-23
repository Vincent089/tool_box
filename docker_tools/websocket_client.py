import asyncio
import websockets

async def hello():
    uri = 'ws://localhost:8000/ws/notifications/?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMjgzY2YzZjEtNjdjYy00NjBkLTg1NmEtODUzYzMwODI4NmQyIiwidXNlcm5hbWUiOiJ2aW5jZW50LmNvcnJpdmVhdSIsImV4cCI6MTYyNTU5NjE0NCwiZW1haWwiOiJ2aW5jZW50LmNvcnJpdmVhdUBjZ2kuY29tIiwib3JpZ19pYXQiOjE2MjU1OTI1NDR9.JuarJpCH8T5XozBCS7c0LC-Ae7sBhPGqMV-YRaXICZY'
    async with websockets.connect(uri) as websocket:
        name = input('What\'s your name? ')

        await websocket.send(name)
        print(f'> %s' % name)

        greeting = await websocket.recv()
        print(f'> %s' % greeting)

asyncio.get_event_loop().run_until_complete(hello())
