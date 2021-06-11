import sys
sys.path.append('.\\Lib\\site-packages')
import websockets
import asyncio
import mapping_flow


ws_uri = 'ws://127.0.0.1:5700'
async def async_processing():
    async with websockets.connect(ws_uri) as websocket:
        while True:
            try:
                message = await websocket.recv()
                await mapping_flow.main_process(message)
                print(message)
            except websockets.ConnectionClosed:
                print('ConnectionClosed')
                break

asyncio.get_event_loop().run_until_complete(async_processing())