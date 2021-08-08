import sys
#导入独立包路径
sys.path.append('.\\Lib\\site-packages')
import websockets
import asyncio
import mapping_flow
import api

platform = api.glo_get("platform")
ws_uri = platform.ws_uri
async def async_processing():
    async with websockets.connect(ws_uri) as websocket:
        while True:
            try:
                message = await websocket.recv()
                #将接受到的信息异步的送入消息匹配流程中
                await mapping_flow.main_process(message)
            except websockets.ConnectionClosed:
                print('ConnectionClosed')
                break

asyncio.get_event_loop().run_until_complete(async_processing())