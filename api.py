import requests
import os, sys, configparser, json
from importlib import import_module

global_dict = {}
match_map ={'private_message':[],
            'group_message':[],
            'group_increase':[]}

#进行全局变量管理
def glo_set(key, value):
    global_dict[key] = value
    return
def glo_get(key, defValue = None):
    try:
        return global_dict[key]
    except KeyError:
        return defValue

#更新匹配结构
def match_update(msg_type: str, key: str, fun: str, match_type = 'reg', priority = 100):
    #优先级越大越优先，默认为100
    #match_map本身类型为承载msg_type触发类型的字典
    #msg_type下则为一个依照优先级顺序排序的列表
    #列表中每个元素对应不同回复的属性字典
    content = {'match_type':match_type, 'key':key, 'function':fun, 'priority':priority}
    if content not in match_map[msg_type]:
        index = -1
        for i in range(0, len(match_map[msg_type])-1):
            #每次插入进行一次独立排序，得到优先级队列
            if match_map[msg_type][i]['priority'] < priority:
                index = i
                break
        match_map[msg_type].insert(index, content)
        print("已导入: %s 的回复" % (key))
    return

def get_match_map():
    return match_map

#############################################


#############################################

#配置初始化
def config_init():
    config = configparser.ConfigParser()
    config.read("./config.ini")
    secs = config.sections()
    if "QQ_config" not in secs:
        #添加不存在的配置节并初始化
        config.add_section("QQ_config")
        config.set("QQ_config", "ws_uri", "ws://127.0.0.1:5700")
        config.set("QQ_config", "http_url", "http://127.0.0.1:5701/")
        #写入配置文件
        f = open('./config.ini', 'w')
        config.write(f)
        f.close()

    opt = config.options("QQ_config")
    if "ws_uri" not in opt:
        config.set("QQ_config", "ws_uri", "ws://127.0.0.1:5700")
    if "http_url" not in opt:
        config.set("QQ_config", "http_url", "http://127.0.0.1:5701/")
    
    ws_uri = config.get("QQ_config", "ws_uri")
    http_url = config.get("QQ_config", "http_url")
    self_id = json.loads(
    requests.get(http_url + 'get_login_info').text
    )['data'].get('user_id',0)
    return [ws_uri, http_url, self_id]

#对象化平台参数
class Platform:
    def __init__(self):
        config_para = config_init()
        self.ws_uri = config_para[0]
        self.http_url = config_para[1]
        self.self_id = config_para[2]
        return
platform = Platform()
glo_set("platform", platform)


#初始化载入插件
class Plugin:
    def __init__(self):
        self.load_dir()

    def load_dir(self):
        for filename in os.listdir("plugins"):
            if not filename.endswith(".zip"):
                continue
            self.load_Plugin(filename)

    def load_Plugin(self, filename:str):
        pluginPath = os.path.join("plugins", filename)
        sys.path.append(pluginPath)
        name = filename.rsplit(".", 1)[0]
        try:
            module = import_module(name)
        except:
            print("插件%s载入出错！"%name)
            return
        print("载入插件%s成功"%name)
        return module

plugin=Plugin()

#######################################


#######################################

#上报通用函数
def post(data, url = platform.http_url):
    headers = {
            'Content-Type': 'application/json'
        }
    res = requests.post(url + data['action'], headers=headers, timeout=5, data=json.dumps(data['params']))
    return res.text

#下载图片到指定temp目录
def download_image():

    return

###############################################


###############################################

#图片cq码
def cq_pic(file):
    return '[CQ:image,file=' + file + ']'

#语音
def cq_voice(file):
    return '[CQ:record,file=' + file + ']'

#AT某人
def cq_at(qq):
    return '[CQ:at,qq=]' + qq + ']'

#回复指定消息

###############################################



###############################################

#私聊消息发送函数封装
def send_private_msg(qq, group, msg):
    data, params= dict(), dict()
    params['user_id'] = qq
    params['group_id'] = group if group else 0
    params['message'] = msg
    data['action'] = 'send_private_msg'
    data['params'] = params
    res = post(data)
    return res

#群聊消息发送
def send_group_msg(group, msg):
    data, params= dict(), dict()
    params['group_id'] = group if group else 0
    params['message'] = msg
    data['action'] = 'send_group_msg'
    data['params'] = params
    res = post(data)
    return res

#撤回消息
def delete_msg(msg_id):
    data, params = dict(), dict()
    params['message_id'] = msg_id
    data['action'] = 'delete_msg'
    data['params'] = params
    res = post(data)
    return res

#获取消息
def get_msg(msg_id):
    data, params = dict(), dict()
    params['message_id'] = msg_id
    data['action'] = 'get_msg'
    data['params'] = params
    res = post(data)
    return res

#获取合并转发内容
def get_forward_msg(msg_id):
    data, params = dict(), dict()
    params['message_id'] = msg_id
    data['action'] = 'get_forward_msg'
    data['params'] = params
    res = post(data)
    return res

#获取图片信息
def get_image(file):
    data, params = dict(), dict()
    params['file'] = file
    data['action'] = 'get_image'
    data['params'] = params
    res = post(data)
    return res

#群组踢人
def set_group_kick(qq, group, reject_add_request = 'false'):
    data, params = dict(), dict()
    params['user_id'] = qq
    params['group_id'] = group
    params['reject_add_request'] = reject_add_request 
    data['action'] = 'set_group_kick'
    data['params'] = params
    post(data)
    return

#群组单人禁言
def set_group_ban(qq, group, duration = '1800'):
    data, params = dict(), dict()
    params['user_id'] = qq
    params['group_id'] = group
    params['duration'] = duration
    data['action'] = 'set_group_ban'
    data['params'] = params
    post(data)
    return

#群组匿名用户禁言
def set_group_anonymous_ban(anonymous, group, flag, duration = '1800'):
    data, params = dict(), dict()
    params['anonymous'] = anonymous
    params['group_id'] = group
    params['flag'] = flag
    params['duration'] = duration
    data['action'] = 'set_group_anonymous_ban'
    data['params'] = params
    post(data)
    return

#群组全体禁言
def set_group_whole_ban(group, enable = 'true'):
    data, params = dict(), dict()
    params['group_id'] = group
    params['enable'] = enable
    data['action'] = 'set_group_whole_ban'
    data['params'] = params
    post(data)
    return

#群组设置管理员
def set_group_admin(group, qq, enable = 'true'):
    data, params = dict(), dict()
    params['group_id'] = group
    params['user_id'] = qq
    params['enable'] = enable
    data['action'] = 'set_group_admin'
    data['params'] = params
    post(data)
    return

#群组匿名
def set_group_anonymous(group, enable = 'true'):
    data, params = dict(), dict()
    params['group_id'] = group
    params['enable'] = enable
    data['action'] = 'set_group_anonymous'
    data['params'] = params
    post(data)
    return

#设置群名片
def set_group_card(group, qq, card = 'true'):
    data, params = dict(), dict()
    params['group_id'] = group
    params['user_id'] = qq
    params['card'] = card
    data['action'] = 'set_group_card'
    data['params'] = params
    post(data)
    return

#设置群名
def set_group_name(group, name):
    data, params = dict(), dict()
    params['group_id'] = group
    params['group_name'] = name
    data['action'] = 'set_group_name'
    data['params'] = params
    post(data)
    return

#设置群头像
def set_group_portrait(group, file, cache = '1'):
    #file支持绝对路径，url和base64
    data, params = dict(), dict()
    params['group_id'] = group
    params['file'] = file
    params['cache'] = cache
    data['action'] = 'set_group_portrait'
    data['params'] = params
    post(data)
    return

#获取登录号信息
def get_login_info():
    data, params = dict(), dict()
    data['action'] = 'get_login_info'
    data['params'] = params
    res = post(data)
    return res

#退群
def set_group_leave(group, is_dismiss = 'false'):
    data, params = dict(), dict()
    params['group_id'] = group
    params['is_dismiss'] = is_dismiss
    data['action'] = 'set_group_leave'
    data['params'] = params
    post(data)
    return

#设群头衔
def set_group_special_title(group, qq, special_title, duration = '-1'):
    data, params = dict(), dict()
    params['group_id'] = group
    params['user_id'] = qq
    params['special_title'] = special_title
    params['duration'] = duration
    data['action'] = 'set_group_special_title'
    data['params'] = params
    post(data)
    return

#处理好友请求
def set_friend_add_request(flag, approve = 'true', remark = ''):
    data, params = dict(), dict()
    params['flag'] = flag
    params['approve'] = approve
    params['remark'] = remark
    data['action'] = 'set_friend_add_request'
    data['params'] = params
    post(data)
    return

#处理群邀请
def set_group_add_request(flag, type, approve = 'true', remark = ''):
    data, params = dict(), dict()
    params['flag'] = flag
    params['type'] = type
    params['approve'] = approve
    params['remark'] = remark
    data['action'] = 'set_group_add_request'
    data['params'] = params
    post(data)
    return

#获取好友列表
def get_friend_list():
    data, params = dict(), dict()
    data['action'] = 'get_friend_list'
    data['params'] = params
    res = post(data)
    return res

#删除好友
def delete_friend(friend_id):
    data, params = dict(), dict()
    params['friend_id'] = friend_id
    data['action'] = 'delete_friend'
    data['params'] = params
    post(data)
    return

#获取群信息
def get_group_info(group, no_cache = 'false'):
    data, params = dict(), dict()
    params['group_id'] = group
    params['no_cache'] = no_cache
    data['action'] = 'get_group_info'
    data['params'] = params
    res = post(data)
    return res

#获取群列表
def get_group_list():
    data, params = dict(), dict()
    data['action'] = 'get_group_list'
    data['params'] = params
    res = post(data)
    return res

#获取群成员信息，要求必须使用群号和QQ号
def get_group_member_info(qq, group, no_cache = 'false'):
    data, params= dict(), dict()
    params['group_id'] = group if group else 0
    params['user_id'] = qq
    params['no_cache'] = no_cache
    data['action'] = 'get_group_member_info'
    data['params'] = params
    res = post(data)
    return res

#陌生人信息获取
def get_stranger_info(qq, no_cache = False):
    data, params= dict(), dict()
    params['user_id'] = qq
    params['no_cache'] = no_cache
    data['action'] = 'get_stranger_info'
    data['params'] = params
    res = post(data)
    return res

#获取群成员列表
def get_group_member_list(group):
    data, params = dict(), dict()
    params['group_id'] = group
    data['action'] = 'get_group_member_list'
    data['params'] = params
    res = post(data)
    return res

#获取群荣誉信息
def get_group_honor_info(group, type = 'all'):
    data, params = dict(), dict()
    params['group_id'] = group
    #talkative performer legend strong_newbie emotion 以分别获取单个类型的群荣誉数据
    #或传入 all 获取所有数据
    params['type'] = type
    data['action'] = 'get_group_honor_info'
    data['params'] = params
    res = post(data)
    return res

#图片ocr
def ocr_image(image):
    #image指图片ID
    data, params = dict(), dict()
    params['image'] = image
    data['action'] = 'ocr_image'
    data['params'] = params
    res = post(data)
    return res

#获取群系统消息
def get_group_system_msg():
    data, params = dict(), dict()
    data['action'] = 'get_group_system_msg'
    data['params'] = params
    res = post(data)
    return res

#上传群文件
def upload_group_file(group, file, name, folder = ''):
    #file为本地路径，name为上传后的文件名，folder为上传目录
    data, params = dict(), dict()
    params['group_id'] = group
    params['file'] = file
    params['name'] = name
    params['folder'] = folder
    data['action'] = 'upload_group_file'
    data['params'] = params
    post(data)
    return

#获取群根目录文件列表
def get_group_root_files(group):
    data, params = dict(), dict()
    params['group_id'] = group
    data['action'] = 'get_group_root_files'
    data['params'] = params
    res = post(data)
    return res

#获取群子目录文件列表
def get_group_files_by_folder(group, folder):
    data, params = dict(), dict()
    params['group_id'] = group
    params['folder_id'] = folder
    data['action'] = 'get_group_files_by_folder'
    data['params'] = params
    res = post(data)
    return res

#获取群文件资源链接
def get_group_file_url(group, file_id, busid):
    data, params = dict(), dict()
    params['group_id'] = group
    params['file_id'] = file_id
    params['busid'] = busid
    data['action'] = 'get_group_file_url'
    data['params'] = params
    res = post(data)
    return res

#获取群文件系统信息
def get_group_file_system_info(group):
    #file为本地路径，name为上传后的文件名，folder为上传目录
    data, params = dict(), dict()
    params['group_id'] = group
    data['action'] = 'get_group_file_system_info'
    data['params'] = params
    res = post(data)
    return res

#发送群公告
def send_group_notice(group, content):
    data, params = dict(), dict()
    params['group_id'] = group
    params['content'] = content
    data['action'] = '_send_group_notice'
    data['params'] = params
    post(data)
    return

#获取群历史消息
def get_group_msg_history(group, message_seq):
    data, params = dict(), dict()
    params['group_id'] = group
    params['message_seq'] = message_seq
    data['action'] = 'get_group_msg_history'
    data['params'] = params
    res = post(data)
    return res

#设置精华消息
def set_essence_msg(message_id):
    data, params = dict(), dict()
    params['message_id'] = message_id
    data['action'] = 'set_essence_msg'
    data['params'] = params
    post(data)
    return

#移除精华消息
def delete_essence_msg(message_id):
    data, params = dict(), dict()
    params['message_id'] = message_id
    data['action'] = 'delete_essence_msg'
    data['params'] = params
    post(data)
    return

#获取状态
def get_status():
    data, params = dict(), dict()
    data['action'] = 'get_status'
    data['params'] = params
    res = post(data)
    return res

#获取版本信息
def get_version_info():
    data, params = dict(), dict()
    data['action'] = 'get_version_info'
    data['params'] = params
    res = post(data)
    return res

#重启CQ
def set_restart(delay = '0'):
    data, params = dict(), dict()
    params['delay'] = delay
    data['action'] = 'set_restart'
    data['params'] = params
    res = post(data)
    return res

###############################################




###############################################

#获取称呼
def get_name(qq, group = 0):
    if group == 0:
        data = get_stranger_info(qq)
        data = json.loads(data)
        res = data['data'].get('nickname', '您')
    else:
        data = get_group_member_info(qq, group)
        data = json.loads(data)
        res = data['data'].get('card', '您')
    return res

#自适应消息发送
def send_msg(qq, group, msg):
    data, params = dict(), dict()
    if group == 0 and qq != 0:
        params['user_id'] = qq
    elif group!=0:
        params['group_id'] = group
    params['message'] = msg
    data['action'] = 'send_msg'
    data['params'] = params
    res = post(data)
    return res

#获取发送者头像
def get_headpic_url(qq, size = '160'):
    #size可以为640、320、40
    url = 'http://q1.qlogo.cn/g?b=qq&nk=' + str(qq) + '&s=' + str(size)
    return url

#######################################


########################################

#已知消息，跟踪用户对象
class MsgUser:
    def __init__(self, data):
        self.qq = data.get('user_id', 0)
        self.group = data.get('group_id', 0)
        return
    #重定向
    def redirect_qq(self, user_id):
        self.qq = user_id
        return
    def redirect_group(self, group_id):
        self.group = group_id
        return
    #自适应回复
    def send(self,msg):
        msg_id = send_msg(self.qq, self.group, msg)
        return msg_id
    #快捷获取昵称
    def name(self):
        if self.name:
            self.name = get_name(self.qq, self.group)
        return self.name


