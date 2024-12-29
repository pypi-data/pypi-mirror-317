from datetime import datetime as datetime
from nonebot.log import logger
import json
import nonebot
from pathlib import Path
from nonebot.adapters.onebot.v11 import PrivateMessageEvent,GroupMessageEvent,MessageEvent
import math
from .conf import private_memory,group_memory,current_directory,main_config,config_dir
__default_config__ = {
    
    "memory_lenth_limit":50,
    "enable":True,
    "poke_reply":True,
    "private_train":{ "role": "system", "content": ""},
    "group_train":{ "role": "system", "content": ""},
    "enable_group_chat":True,
    "enable_private_chat":True,
    "allow_custom_prompt":True,
    "allow_send_to_admin":True,
    "admin_group":0,
    "admins":[],
    "open_ai_base_url":"",
    "open_ai_api_key":"",
    "say_after_self_msg_be_deleted":True,
    "after_deleted_say_what":[ 
    "Suggar说错什么话了吗～下次我会注意的呢～",  
    "抱歉啦，不小心说错啦～",  
    "嘿，发生什么事啦？我",  
    "唔，我是不是说错了什么？",  
    "纠错时间到，如果我说错了请告诉我！",  
    "发生了什么？我刚刚没听清楚呢~",  
    "我能帮你做点什么吗？不小心说错话了让我变得不那么尴尬~",  
    "我会记住的，绝对不再说错话啦~",  
    "哦，看来我又犯错了，真是不好意思！",  
    "哈哈，看来我得多读书了~",  
    "哎呀，真是个小口误，别在意哦~",  
    "Suggar苯苯的，偶尔说错话很正常嘛！",    
    "哎呀，我也有尴尬的时候呢~",  
    "希望我能继续为你提供帮助，不要太在意我的小错误哦！",  
    ]  
}
def get_config()->dict:
    f"""
    获取配置文件

    Returns:
    dict: 配置文件，包含以下键值对{__default_config__}
        

    """

    if not Path(config_dir).exists():
        Path.mkdir(config_dir)
        with open(str(main_config),"w",encoding="utf-8") as f:
            json.dump(__default_config__,f,ensure_ascii=False,indent=4)
    with open(str(main_config),"r",encoding="utf-8") as f:
           conf = json.load(f)
           return conf
def get_memory_data(event:MessageEvent)->dict:
    """
    根据消息事件获取记忆数据，如果用户或群组的记忆数据不存在，则创建初始数据结构

    参数:
    event: MessageEvent - 消息事件，可以是私聊消息事件或群聊消息事件，通过事件解析获取用户或群组ID

    返回:
    dict - 用户或群组的记忆数据字典
    """
       # 检查私聊记忆目录是否存在，如果不存在则创建
    if not Path(private_memory).exists() or not Path(private_memory).is_dir():
        Path.mkdir(private_memory)
    
    # 检查群聊记忆目录是否存在，如果不存在则创建
    if not Path(group_memory).exists() or not Path(group_memory).is_dir():
        Path.mkdir(group_memory)
    
    # 根据事件类型判断是私聊还是群聊
    if isinstance(event, PrivateMessageEvent):
        # 处理私聊事件
        user_id = event.user_id
        conf_path = Path(private_memory/f"{user_id}.json")
        # 如果私聊记忆数据不存在，则创建初始数据结构
        if not conf_path.exists():
            with open(str(conf_path), "w", encoding="utf-8") as f:
                json.dump({"id": user_id, "enable": True, "memory": {"messages": []}, 'full': False}, f, ensure_ascii=True, indent=0)
    else:
        # 处理群聊事件
        group_id = event.group_id
        conf_path = Path(group_memory/f"{group_id}.json")
        # 如果群聊记忆数据不存在，则创建初始数据结构
        if not conf_path.exists():
            with open(str(conf_path), "w", encoding="utf-8") as f:
                json.dump({"id": group_id, "enable": True, "memory": {"messages": []}, 'full': False}, f, ensure_ascii=True, indent=0)
    
    # 读取并返回记忆数据
    with open(str(conf_path), "r", encoding="utf-8") as f:
        conf = json.load(f)
        return conf
def write_memory_data(event: MessageEvent, data: dict) -> None:
    """
    根据事件类型将数据写入到特定的记忆数据文件中。
    
    该函数根据传入的事件类型（群组消息事件或用户消息事件），将相应的数据以JSON格式写入到对应的文件中。
    对于群组消息事件，数据被写入到以群组ID命名的文件中；对于用户消息事件，数据被写入到以用户ID命名的文件中。
    
    参数:
    - event: MessageEvent类型，表示一个消息事件，可以是群组消息事件或用户消息事件。
    - data: dict类型，要写入的数据，以字典形式提供。
    
    返回值:
    无返回值。
    """
    # 判断事件是否为群组消息事件
    if isinstance(event, GroupMessageEvent):
        # 获取群组ID，并根据群组ID构造配置文件路径
        group_id = event.group_id
        conf_path = Path(private_memory/f"{group_id}.json")
    else:
        # 获取用户ID，并根据用户ID构造配置文件路径
        user_id = event.user_id
        conf_path = Path(private_memory/f"{user_id}.json")
    
    # 打开配置文件路径对应的文件，以写入模式，并确保文件以UTF-8编码
    with open(str(conf_path), "w", encoding="utf-8") as f:
        # 将数据写入到文件中，确保ASCII字符以外的字符也能被正确处理
        json.dump(data, f, ensure_ascii=True)




async def get_friend_info(qq_number: int)->str:
    bot = nonebot.get_bot()  # 假设只有一个Bot实例运行
    friend_list = await bot.get_friend_list()
    
    for friend in friend_list:
        if friend['user_id'] == qq_number:
            return friend['nickname']  # 返回找到的好友的昵称
    
    return None 

async def get_friend_qq_list():  
    bot = nonebot.get_bot()  
    friend_list = await bot.get_friend_list()  
    friend_qq_list = [friend['user_id'] for friend in friend_list]  
    return friend_qq_list 
def split_list(lst:list, threshold:int) -> list:
    """
    将列表分割成多个子列表，每个子列表的最大长度不超过threshold。
    
    :param lst: 原始列表
    :param threshold: 子列表的最大长度
    :return: 分割后的子列表列表
    """
    if len(lst) <= threshold:
        return [lst]
    
    result = []
    for i in range(0, len(lst), threshold):
        chunk = lst[i:i + threshold]
        result.append(chunk)
    
    return result

def get_love_level(exp: int) -> int:
    a = 0.3  # 常数 a 
    if exp < 0:
        exp = str(exp).lstrip("-")
        level = int(math.sqrt(abs(int(exp)) / a))
        return -level
    level = int(math.sqrt(exp / a))
    return level
def get_level(exp: int) -> int:
    a = 10  # 常数 a 
    level = int(math.sqrt(exp / a))
    return level
async def get_group_member_qq_numbers(group_id: int) -> list[int]:
    """
    获取指定群组的所有成员QQ号列表
    
    :param group_id: 群组ID
    :return: 成员QQ号列表
    """
    bot = nonebot.get_bot()  # 获取当前机器人实例
    member_list = await bot.get_group_member_list(group_id=group_id)
    
    # 提取每个成员的QQ号
    qq_numbers = [member['user_id'] for member in member_list]
    
    return qq_numbers
async def is_same_day(timestamp1:int, timestamp2:int) -> bool:
    # 将时间戳转换为datetime对象，并只保留日期部分
    date1 = datetime.fromtimestamp(timestamp1).date()
    date2 = datetime.fromtimestamp(timestamp2).date()
    
    # 比较两个日期是否相同
    return date1 == date2
async def synthesize_forward_message(forward_msg:dict) -> str:
    forw_msg = {'messages': [{'content': [{'type': 'text', 'data': {'text': 'Prompt:\n这里是Leaves的社区群。leaves是什么？Leaves 是基于 Paper 的 Minecraft 服务端，旨在修复被破坏的原版特性。为什么选择 Leaves？\n速度快得离谱\nLeaves 包含大量改进和优化，从而显著提高了性能。这包括异步区块加载，以及对光照引擎、漏斗、实体等的重要改进。\n扩展应用程序接口\nLeaves 扩展并改进了 Bukkit、Spigot 和 Paper 应用程序接口，使您和开发者可以随心所欲地使用更多特性和功能，Leaves服务端不能安装模组！。\n你需要为群友解决问题，这里是Leaves文档的链接：https://docs.leavesmc.org/leaves/guides/getting-started\nLeaves与Leaf服务端是两个不同的服务端'}}], 'sender':{'nickname': 'Suggar', 'user_id': 2516251531}, 'time': 1729994618, 'message_format': 'array', 'message_type': 'group'}]}
    forw_msg = forward_msg
    # 初始化最终字符串
    result = ""
    
    # forward_msg 是一个包含多个消息段的字典+列表
    for segment in forw_msg['messages']:
        
        
        nickname = segment['sender']['nickname']
        qq = segment['sender']['user_id']
        time = f"[{datetime.fromtimestamp(segment['time']).strftime('%Y-%m-%d %I:%M:%S %p')}]"
        result += f"{time}[{nickname}({qq})]说："
        for segments in segment['content']:
         segments_type = segments['type']
         if segments_type == "text":
            result += f"{segments['data']['text']}"
         
         elif segments_type == "at":
            result += f" [@{segments['data']['qq']}]"

         
        result += "\n"

        
        
    return result

def get_current_datetime_timestamp():
    # 获取当前时间
    now = datetime.now()

    # 格式化日期、星期和时间
    formatted_date = now.strftime("%Y-%m-%d")
    formatted_weekday = now.strftime("%A")
    formatted_time = now.strftime("%I:%M:%S %p")

    # 组合格式化的字符串
    formatted_datetime = f"[{formatted_date} {formatted_weekday} {formatted_time}]"

    return formatted_datetime
