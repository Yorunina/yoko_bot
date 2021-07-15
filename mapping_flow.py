import json
from script import *
import re
import api

bot_id = str(api.glo_get('self_id'))
at_id = '[CQ:at,qq=' + bot_id + ']'
match_map = api.get_match_map()
match_flow_private = match_map['private']
match_flow_group = match_map['group']
print(match_map)
async def common_event():
    pass
async def unknown_event():
    pass
async def default():
    pass


async def flow_deal(data, command:str, flow):
    for obj in flow:
        key = obj['key']
        #进行正则匹配
        if obj['match_type'] == 'reg':
            #正则表达式匹配
            match_obj = re.match(key, command, re.M|re.I)
            #如果成功
            if match_obj:
                #调用函数
                await obj['function'](data, command)
                break
        #进行完全匹配
        if obj['match_type'] == 'abs' and command == key:
            await obj['function'](data, command)
            break
        #进行前缀匹配
        if obj['match_type'] == 'pre' and command.startswith(key):
            await obj['function'](data, command)
            break
    return

#戳一戳事件处理
async def poke_event(data):
    await setu.setu(data, False)
    return

async def private_event(data):
    msg = str(data['message'])
    #多匹配机制
    if msg.startswith(('.', '。')):
        #清除空格和首位
        command = msg[1:].strip()
        #进行循环匹配
        await flow_deal(data, command, match_flow_private)
    return



async def group_event(data):
    msg = str(data['message'])
    #清除前缀干扰并且添加at标识
    if msg.startswith(at_id):
        msg = msg.rstrip(at_id).strip()
        flag_at = True
    #多匹配机制
    if msg.startswith(('.', '。')):
        #清除空格和首位
        command = msg[1:].strip()
        #进行循环匹配
        await flow_deal(data, command, match_flow_group)
    return

async def main_process(ori_data):
    if ori_data:
        data = json.loads(ori_data)
        if data['post_type'] == 'notice':
            if data['notice_type'] == 'notify':
                if data['sub_type'] == 'poke':
                    #戳一戳事件
                    await poke_event(data)
                elif data['sub_type'] == 'lucky_king':
                    #运气王事件
                    await common_event()
                elif data['sub_type'] == 'honor':
                    #群荣耀变化事件
                    await common_event()
                else:
                    await unknown_event()
            elif data['notice_type'] == 'group_upload':
                #群文件上传事件
                await common_event()
            elif data['notice_type'] == 'group_admin':
                #群管理变动事件
                await common_event()
            elif data['notice_type'] == 'group_increase':
                #群成员增加事件
                await common_event()
            elif data['notice_type'] == 'group_decrease':
                #群成员减少事件
                await common_event()
            elif data['notice_type'] == 'group_ban':
                #群成员禁言事件
                await common_event()
            elif data['notice_type'] == 'friend_add':
                #好友添加事件
                await common_event()
            elif data['notice_type'] == 'group_recall':
                #群撤回事件
                await common_event()
            elif data['notice_type'] == 'friend_recall':
                #好友撤回事件
                await common_event()
            elif data['notice_type'] == 'group_card':
                #群成员名片更新
                await common_event()
            elif data['notice_type'] == 'offline_file':
                #接收到离线文件
                await common_event()
            elif data['notice_type'] == 'client_status':
                #客户端状态改变
                await common_event()
            else:
                await unknown_event()
        elif data['post_type'] == 'request':
            if data['request_type'] == 'friend':
                #好友添加请求
                await common_event()
            elif data['request_type'] == 'group':
                #群添加请求
                await common_event()
            else:
                await unknown_event()
        elif data['post_type'] == 'message':
            if data['message_type'] == 'private':
                #私聊消息
                await private_event(data)
            elif data['message_type'] == 'group':
                #群聊消息
                await group_event(data)
            else:
                await unknown_event()
        else:
            await unknown_event()
    return