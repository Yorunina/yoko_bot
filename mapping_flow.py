import json, api, re

platform = api.glo_get("platform")
bot_id = str(platform.self_id)
at_id = '[CQ:at,qq=' + bot_id + ']'
match_map = api.get_match_map()
print(match_map)

def unknown_event(data):
    pass
def default():
    pass

def flow_deal(data, command:str, flow):
    for obj in flow:
        key = obj['key']
        #进行正则匹配
        if obj['match_type'] == 'reg':
            #正则表达式匹配
            match_obj = re.match(key, command, re.M|re.I)
            #如果成功
            if match_obj:
                #调用函数
                obj['function'](data, command)
                break
        #进行完全匹配
        if obj['match_type'] == 'abs' and command == key:
            obj['function'](data, command)
            break
        #进行前缀匹配
        if obj['match_type'] == 'pre' and command.startswith(key):
            obj['function'](data, command)
            break
    return

#私聊事件
def private_event(data):
    msg = str(data['message'])
    #多匹配机制
    if msg.startswith(('.', '。')):
        #清除空格和首位
        command = msg[1:].strip()
        #进行循环匹配
        flow_deal(data, command, match_map['private_message'])
    return

#群聊事件
def group_event(data):
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
        flow_deal(data, command, match_map['group_message'])
    return

#无匹配常规事件
def common_event(data):
    if data['post_type'] == 'request':
        event_type = data['request_type']
    else:
        if data['sub_type'] == 'notify':
            event_type = data['sub_type']
        else:
            event_type = data['notice_type']
    
    #for obj in match_map[event_type]:
    #    obj['function'](data, '')
    return

#戳一戳事件处理
def notify_event(data):
    #setu.setu(data, False)
    return

def match_process(ori_data):
    if ori_data:
        data = json.loads(ori_data)
        if data['post_type'] == 'notice':
            if data['notice_type'] == 'notify':
                if data['sub_type'] == 'poke':
                    #戳一戳事件
                    notify_event(data)
                elif data['sub_type'] == 'lucky_king':
                    #运气王事件
                    common_event(data)
                elif data['sub_type'] == 'honor':
                    #群荣耀变化事件
                    common_event(data)
                else:
                    unknown_event(data)
            elif data['notice_type'] == 'group_upload':
                #群文件上传事件
                common_event(data)
            elif data['notice_type'] == 'group_admin':
                #群管理变动事件
                common_event(data)
            elif data['notice_type'] == 'group_increase':
                #群成员增加事件
                common_event(data)
            elif data['notice_type'] == 'group_decrease':
                #群成员减少事件
                common_event(data)
            elif data['notice_type'] == 'group_ban':
                #群成员禁言事件
                common_event(data)
            elif data['notice_type'] == 'friend_add':
                #好友添加事件
                common_event(data)
            elif data['notice_type'] == 'group_recall':
                #群撤回事件
                common_event(data)
            elif data['notice_type'] == 'friend_recall':
                #好友撤回事件
                common_event(data)
            elif data['notice_type'] == 'group_card':
                #群成员名片更新
                common_event(data)
            elif data['notice_type'] == 'offline_file':
                #接收到离线文件
                common_event(data)
            elif data['notice_type'] == 'client_status':
                #客户端状态改变
                common_event(data)
            else:
                unknown_event(data)
        elif data['post_type'] == 'request':
            if data['request_type'] == 'friend':
                #好友添加请求
                common_event(data)
            elif data['request_type'] == 'group':
                #群添加请求
                common_event(data)
            else:
                unknown_event(data)
        elif data['post_type'] == 'message':
            if data['message_type'] == 'private':
                #私聊消息
                private_event(data)
            elif data['message_type'] == 'group':
                #群聊消息
                group_event(data)
            else:
                unknown_event(data)
        else:
            unknown_event(data)
    return