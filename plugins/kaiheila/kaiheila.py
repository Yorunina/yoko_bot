import api
import json
import aiohttp
import configparser
from sys import path
#导入独立包路径
path.append('.\\Lib')

async def http_get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            res = await resp.text()
            return res

def config_init():
    config = configparser.ConfigParser()
    config.read("./config/kaiheila/config.ini")
    secs = config.sections()
    id = 0
    if "tools" in secs:
        opt = config.options("tools")
        if "id" in opt:
            id = config.get("tools", "id")
        else:
            print("开黑啦插件未检测到可用小工具id！")
    else:
        print("开黑啦插件未检测到可用小工具id！")
    return id


id = config_init()
group = 318534265
url = "https://www.kaiheila.cn/api/guilds/" + id
old_player_list = []
state = 1

class kaiheila:
    async def play_what(data, command_obj):
        appenstr = ""
        try:
            json_data = await http_get(url)
            play_data = json.loads(json_data)
            user = api.MsgUser(data)
            for channel in play_data["channels"]:
                if "users" not in channel:
                    continue
                else:
                    appenstr = appenstr + "\n" + channel["name"] + "：" + len(channel["users"])
            if not appenstr:
                appenstr = "\n但是似乎并没有人在游戏中呢~"
            await user.send("当前在线人数：" + play_data["online_count"] + appenstr)
        except:
            return
        return

    async def get_player_list_update():
        global old_player_list
        player_list = []
        update_list = []
        try:
            http_data = await http_get(url)
            player_data = json.loads(http_data)
            
            for channel in player_data["channels"]:
                    if "users" not in channel:
                        continue
                    else:
                        channel_name = channel["name"]
                        player_list.append(channel_name)
                        if channel_name not in old_player_list:
                            update_list.append(channel_name)
        except:
            return []
        if player_list != old_player_list:
            old_player_list = player_list
        return update_list

    async def listen_update():
        update_list = await kaiheila.get_player_list_update()
        if update_list:
            await api.send_group_msg(group, ",".join(update_list))
        return

    async def listen_update_on(data, command_obj):
        global state
        user = api.MsgUser(data)
        if state == 1:
            await user.send("已开启监听服务了哦√")
        else:
            state = 1
            await user.send("开启监听服务√")

    async def listen_update_off(data, command_obj):
        state = 0
        user = api.MsgUser(data)
        await user.send("关闭监听服务√")



class plugin_load:
#匹配类型：私聊、匹配依据：setu、调用函数：send_setu、匹配方式：前缀匹配：prefix、匹配优先级：50（越大越优先）
    def __init__(self):
        api.match_update('private_message', 'whl', kaiheila.play_what, 'pre', 50)
        api.match_update('group_message', 'whl', kaiheila.play_what, 'pre', 50)
        api.match_update('group_message', 'lon', kaiheila.listen_update_on, 'pre', 50)
        api.match_update('group_message', 'loff', kaiheila.listen_update_off, 'pre', 50)
        return

if __name__ != "__main__":
    plugin_load()