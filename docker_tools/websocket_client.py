import asyncio
import websockets

async def hello():
    uri = 'ws://172.27.49.134:80/ws/vlans'
    async with websockets.connect(uri) as websocket:
        name = input('What\'s your name? ')

        await websocket.send(name)
        print(f'> %s' % name)

        greeting = await websocket.recv()
        print(f'> %s' % greeting)

asyncio.get_event_loop().run_until_complete(hello())
