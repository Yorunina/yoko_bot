import json
import aiohttp
import asyncio

secret = 'ej222222'
http_url = 'http://127.0.0.1:5701/'
self_id = '1660441756'

def get_self_id(bot_id = self_id):
    return bot_id

async def post(data, url = http_url):
    async with aiohttp.ClientSession() as session:
        headers = {
            'Content-Type': 'application/json'
        }
        jdata = json.dumps(data['params'])
        async with session.post(url + data['action'], data=jdata, headers=headers) as response:
            res = response.text
    return res

#图片cq码
async def cq_pic(url):
    return '[CQ:image,file=' + url + ']'

#私聊消息发送函数封装
async def send_private_msg(qq, group, msg):
    data, params= dict(), dict()
    params['user_id'] = qq
    params['group_id'] = group if group else 0
    params['message'] = msg
    data['action'] = 'send_private_msg'
    data['params'] = params
    res = await post(data)
    return res

async def send_group_msg(group, msg):
    data, params= dict(), dict()
    params['group_id'] = group if group else 0
    params['message'] = msg
    data['action'] = 'send_group_msg'
    data['params'] = params
    res = await post(data)
    return res

async def send_msg(qq, group, msg):
    data, params = dict(), dict()
    if group == 0 and qq!=0:
        params['user_id'] = qq
    elif group!=0:
        params['group_id'] = group
    params['message'] = msg
    data['action'] = 'send_msg'
    data['params'] = params
    res = await post(data)
    return res

#消息用户对象
class MsgUser:
    def __init__(self, data):
        self.qq = data.get('user_id', 0)
        self.group = data.get('group_id', 0)
        return
    #重定向
    async def redirect_qq(self, user_id):
        self.qq = user_id
        return
    async def redirect_group(self, group_id):
        self.group = group_id
        return
    #以对象为参数的自适应回复
    async def send(self,msg):
        await send_msg(self.qq, self.group, msg)
        return

