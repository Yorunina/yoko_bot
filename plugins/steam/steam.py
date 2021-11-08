import asyncio,aiohttp
import json

key = "73C176570BFF37F2A9233E3E6901274F"
steamid = "76561198321086250"

async def http_get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            res = await resp.text()
            return res


#获取用户信息
async def GetPlayerSummaries(steamid):
    #包含以下属性(response.players)
    #steamid：输入steamid，64位id
    #communityvisibilitystate：社区可见程度
    #profilestate：个人资料状态
    #personaname：你 の 名 字
    #commentpermission：是否允许在资料页评论
    #profileurl：个人资料网页url
    #avatar、avatarmedium、avatarfull、avatarhash：头像
    #lastlogoff、timecreated：最后下线时间、账号创造时间
    #personastate、personastateflags：当前状态
    #realname、primaryclanid：真名、什么初始id(不知道)
    #loccountrycode、locstatecode、loccityid
    ori_data =  await http_get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=" + key + "&steamids=" + steamid)
    data = json.loads(ori_data)
    return data

#获取游戏库存
async def GetOwnedGames(steamid):
    #包含以下属性(response)
    #game_count：游戏数量
    #games.appid：游戏的appid
    #games.playtime_forever：总游戏时长
    #games.playtime_windows_forever、playtime_linux_foreverplaytime_mac_forever：三平台
    ori_data =  await http_get("http://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key=" + key + "&steamid=" + steamid)
    data = json.loads(ori_data)
    return data

#获取最近游玩
async def GetRecentlyPlayedGames(steamid):
    ori_data =  await http_get("http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1/?key=" + key + "&steamid=" + steamid)
    data = json.loads(ori_data)
    return data

#获取好友列表
async def GetFriendList(steamid):
    ori_data =  await http_get("http://api.steampowered.com/ISteamUser/GetFriendList/v1/?key=" + key + "&steamid=" + steamid)
    data = json.loads(ori_data)
    return data

#获取好友列表
async def GetPlayerSummaries(steamid):
    ori_data =  await http_get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=" + key + "&steamids=" + steamid)
    data = json.loads(ori_data)
    return data


async def main():
    print(await GetPlayerSummaries(steamid))

if __name__ == '__main__':
    #API列表
    #url = "http://api.steampowered.com/ISteamWebAPIUtil/GetSupportedAPIList/v1/?key=" + key + "&steamids=" + steamid
    loop =  asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(main())
    loop.close()




