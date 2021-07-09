import sys
#导入独立包路径
sys.path.append('.\\Lib\\site-packages')
import websockets
import asyncio
import mapping_flow
import api

ws_uri = api.glo_get('ws_uri')
async def async_processing():
    async with websockets.connect(ws_uri) as websocket:
        while True:
            try:
                message = await websocket.recv()
                await mapping_flow.main_process(message)
            except websockets.ConnectionClosed:
                print('ConnectionClosed')
                break

asyncio.get_event_loop().run_until_complete(async_processing())