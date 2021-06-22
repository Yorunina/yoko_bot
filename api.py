import json
import aiohttp
import asyncio
import re
import requests

secret = ''
ws_uri = 'ws://127.0.0.1:5700'
http_url = 'http://127.0.0.1:5701/'
self_id = json.loads(requests.get(http_url + 'get_login_info').text)['data'].get('user_id',0)

def get_self_id(bot_id = self_id):
    return bot_id

def get_http_url(url = http_url):
    return url

def get_ws_uri(ws = ws_uri):
    return ws

async def post(data, url = http_url):
    async with aiohttp.ClientSession() as session:
        headers = {
            'Content-Type': 'application/json'
        }
        jdata = json.dumps(data['params'])
        async with session.post(url + data['action'], data=jdata, headers=headers) as response: 
            return await response.text()

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

#群聊消息发送
async def send_group_msg(group, msg):
    data, params= dict(), dict()
    params['group_id'] = group if group else 0
    params['message'] = msg
    data['action'] = 'send_group_msg'
    data['params'] = params
    res = await post(data)
    return res

#自适应消息发送
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

#撤回消息
async def delete_msg(msg_id):
    data, params = dict(), dict()
    params['message_id'] = msg_id
    data['action'] = 'delete_msg'
    data['params'] = params
    res = await post(data)
    return res

#获取消息
async def get_msg(msg_id):
    data, params = dict(), dict()
    params['message_id'] = msg_id
    data['action'] = 'get_msg'
    data['params'] = params
    res = await post(data)
    return res

#获取合并转发内容
async def get_forward_msg(msg_id):
    data, params = dict(), dict()
    params['message_id'] = msg_id
    data['action'] = 'get_forward_msg'
    data['params'] = params
    res = await post(data)
    return res

#获取图片信息
async def get_image(file):
    data, params = dict(), dict()
    params['file'] = file
    data['action'] = 'get_image'
    data['params'] = params
    res = await post(data)
    return res

#群组踢人
async def set_group_kick(qq, group, reject_add_request = 'false'):
    data, params = dict(), dict()
    params['user_id'] = qq
    params['group_id'] = group
    params['reject_add_request'] = reject_add_request 
    data['action'] = 'set_group_kick'
    data['params'] = params
    await post(data)
    return

#群组单人禁言
async def set_group_ban(qq, group, duration = '1800'):
    data, params = dict(), dict()
    params['user_id'] = qq
    params['group_id'] = group
    params['duration'] = duration
    data['action'] = 'set_group_ban'
    data['params'] = params
    await post(data)
    return

#群组匿名用户禁言
async def set_group_anonymous_ban(anonymous, group, flag, duration = '1800'):
    data, params = dict(), dict()
    params['anonymous'] = anonymous
    params['group_id'] = group
    params['flag'] = flag
    params['duration'] = duration
    data['action'] = 'set_group_anonymous_ban'
    data['params'] = params
    await post(data)
    return

#群组全体禁言
async def set_group_whole_ban(group, enable = 'true'):
    data, params = dict(), dict()
    params['group_id'] = group
    params['enable'] = enable
    data['action'] = 'set_group_whole_ban'
    data['params'] = params
    await post(data)
    return

#群组设置管理员
async def set_group_admin(group, qq, enable = 'true'):
    data, params = dict(), dict()
    params['group_id'] = group
    params['user_id'] = qq
    params['enable'] = enable
    data['action'] = 'set_group_admin'
    data['params'] = params
    await post(data)
    return

#群组匿名
async def set_group_anonymous(group, enable = 'true'):
    data, params = dict(), dict()
    params['group_id'] = group
    params['enable'] = enable
    data['action'] = 'set_group_anonymous'
    data['params'] = params
    await post(data)
    return

#设置群名片
async def set_group_card(group, qq, card = 'true'):
    data, params = dict(), dict()
    params['group_id'] = group
    params['user_id'] = qq
    params['card'] = card
    data['action'] = 'set_group_card'
    data['params'] = params
    await post(data)
    return

#设置群名
async def set_group_name(group, name):
    data, params = dict(), dict()
    params['group_id'] = group
    params['group_name'] = name
    data['action'] = 'set_group_name'
    data['params'] = params
    await post(data)
    return

#获取登录号信息
async def get_login_info():
    data, params = dict(), dict()
    data['action'] = 'get_login_info'
    data['params'] = params
    res = await post(data)
    return res

#退群
async def set_group_leave(group, is_dismiss = 'false'):
    data, params = dict(), dict()
    params['group_id'] = group
    params['is_dismiss'] = is_dismiss
    data['action'] = 'set_group_leave'
    data['params'] = params
    await post(data)
    return

#设群头衔
async def set_group_special_title(group, qq, special_title, duration = '-1'):
    data, params = dict(), dict()
    params['group_id'] = group
    params['user_id'] = qq
    params['special_title'] = special_title
    params['duration'] = duration
    data['action'] = 'set_group_special_title'
    data['params'] = params
    await post(data)
    return

#处理好友请求
async def set_friend_add_request(flag, approve = 'true', remark = ''):
    data, params = dict(), dict()
    params['flag'] = flag
    params['approve'] = approve
    params['remark'] = remark
    data['action'] = 'set_friend_add_request'
    data['params'] = params
    await post(data)
    return

#处理群邀请
async def set_group_add_request(flag, type, approve = 'true', remark = ''):
    data, params = dict(), dict()
    params['flag'] = flag
    params['type'] = type
    params['approve'] = approve
    params['remark'] = remark
    data['action'] = 'set_group_add_request'
    data['params'] = params
    await post(data)
    return

#获取群成员信息，要求必须使用群号和QQ号
async def get_group_member_info(qq, group, no_cache = 'false'):
    data, params= dict(), dict()
    params['group_id'] = group if group else 0
    params['user_id'] = qq
    params['no_cache'] = no_cache
    data['action'] = 'get_group_member_info'
    data['params'] = params
    res = await post(data)
    return res

#陌生人信息获取
async def get_stranger_info(qq, no_cache = False):
    data, params= dict(), dict()
    params['user_id'] = qq
    params['no_cache'] = no_cache
    data['action'] = 'get_stranger_info'
    data['params'] = params
    res = await post(data)
    return res

#获取称呼
async def get_name(qq, group = 0):
    if group == 0:
        data = await get_stranger_info(qq)
        data = json.loads(data)
        res = data['data'].get('nickname', '您')
    else:
        data = await get_group_member_info(qq, group)
        data = json.loads(data)
        res = data['data'].get('card', '您')
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
        msg_id = await send_msg(self.qq, self.group, msg)
        return msg_id
    #快捷获取昵称
    async def name(self):
        if self.name:
            self.name = await get_name(self.qq, self.group)
        return self.name


