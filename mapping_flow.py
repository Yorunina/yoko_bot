import json
from script import *
import re
import api

bot_id = str(api.get_self_id())

match_flow_group = {}
match_flow_private = {}
match_flow_all = {'setu':setu.send_setu,
                  'bsetu':setu.send_bsetu}

match_flow_group.update(match_flow_all)
match_flow_private.update(match_flow_all)

async def common_event():
    return
async def unknown_event():
    return
async def default():
    return


#戳一戳事件处理
async def poke_event(data):
    await setu.setu(data, False)
    return

async def private_event(data):
    msg = str(data['message'])
    command_obj = re.match('(?:\[CQ:at,qq=' + bot_id + '\])?\s*[\.。](.+)', msg, re.M|re.I)
    if command_obj:
        #获取前缀外的子关键词
        command = command_obj.group(1)
        for key in match_flow_private:
            #进行正则序列匹配
            match_obj = re.match(key, command, re.M|re.I)
            if match_obj:
                #匹配成功，传入键值并且传入子关键词
                await match_flow_private[key](data, command_obj)
                #匹配成功后即刻中断
                break
    return


async def group_event(data):
    msg = str(data['message'])
    command_obj = re.match('(?:\[CQ:at,qq=' + bot_id + '\])?\s*[\.。](.+)', msg, re.M|re.I)
    if command_obj:
        command = command_obj.group(1)
        for key in match_flow_group:
            match_obj = re.match(key, command, re.M|re.I)
            if match_obj:
                await match_flow_group[key](data, command_obj)
                break
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
