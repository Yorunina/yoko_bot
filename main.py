from sys import path
#导入独立包路径
path.append('.\\Lib')
import websockets
import asyncio
import threading, configparser
from multiprocessing import Process, Pipe
from importlib import import_module


def get_ws_uri():
    config = configparser.ConfigParser()
    config.read("./config.ini")
    secs = config.sections()
    if "QQ_config" not in secs:
        #添加不存在的配置节并初始化
        config.add_section("QQ_config")
        config.set("QQ_config", "ws_uri", "ws://127.0.0.1:5700")
        f = open('./config.ini', 'w')
        config.write(f)
        f.close()

    opt = config.options("QQ_config")
    if "ws_uri" not in opt:
        config.set("QQ_config", "ws_uri", "ws://127.0.0.1:5700")
    ws_uri = config.get("QQ_config", "ws_uri")
    return ws_uri

async def async_processing(conn_queu):
    async with websockets.connect(get_ws_uri()) as websocket:
        while True:
            try:
                message = await websocket.recv()
                #将接受到的信息异步的送入消息匹配流程中
                conn_queu.send(message)
                
            except websockets.ConnectionClosed:
                print('ConnectionClosed')
                break

def get_conn(conn_queu):
    loop =  asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_processing(conn_queu))
    return



def process_main():
    mapping_flow = import_module('mapping_flow')
    conn_queue, msg_queue = Pipe()
    conn_process = Process(target=get_conn, args=(conn_queue,))
    conn_process.start()
    while True:
        msg =  msg_queue.recv()
        #print("\033[32mINFO:" + msg + "\033[0m")
        match_loop = threading.Thread(target = mapping_flow.match_process, args = [msg])
        match_loop.start()
 
 
 
if __name__ == '__main__':
    process_main()
