import sqlite3
import re
import api

class setu:
    def find_setu(data, r_18 = False):
        #建立数据库连接
        conn = sqlite3.connect('.\\database\\setu.db')
        #获取游标对象
        cursor = conn.cursor()
        state = 'SETU' if r_18 else 'SETU2'
        #随机提取色图
        sql_sen = 'SELECT * FROM ' + state + ' ORDER BY RANDOM() limit 1;'
        cursor.execute(sql_sen)
        value = cursor.fetchall()
        ori_url = value[0][3]
        pid = str(value[0][0])
        #根据footer和pid重新拼接新的储存桶链接
        footer_obj = re.search('_p\d(\.[a-z]{3})',ori_url,re.M|re.I)
        footer = footer_obj.group(1)
        url = 'https://picbucket-1257117970.cos.ap-beijing.myqcloud.com/' + pid + footer
        #建立消息对象
        user = api.MsgUser(data)
        user.send(api.cq_pic(url))
        #关闭数据库服务
        conn.close()
        return

        #用于异步调用的函数
    def send_setu(data, command_obj):
        setu.find_setu(data, False)
        return
    def send_setub(data, command_obj):
        setu.find_setu(data, True)
        return

class plugin_load:
#匹配类型：私聊、匹配依据：setu、调用函数：send_setu、匹配方式：前缀匹配：prefix、匹配优先级：50（越大越优先）
    def __init__(self):
        api.match_update('private_message', 'setu', setu.send_setu, 'pre', 50)
        api.match_update('private_message', 'setub', setu.send_setub, 'pre', 50)
        api.match_update('group_message', 'setu', setu.send_setu, 'pre', 50)
        return

if __name__ != "__main__":
    plugin_load()