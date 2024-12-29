from nonebot import on_command,on_notice,on_message,get_driver,on_request
import nonebot.adapters
from nonebot.rule import to_me
from nonebot.adapters import Message,Event
from nonebot.params import CommandArg
from .resources import get_current_datetime_timestamp,\
     get_friend_info,synthesize_forward_message,get_memory_data,write_memory_data
from .import resources
from nonebot.adapters.onebot.v11 import Message, MessageSegment, GroupMessageEvent,  \
    GroupIncreaseNoticeEvent, Bot, \
    PokeNotifyEvent,GroupRecallNoticeEvent\
    , MessageEvent
from nonebot import logger
from nonebot.matcher import Matcher
import yaml
import sys
import openai
import random
import os
from datetime import datetime  

config = resources.get_config()

async def send_to_admin(msg:str)-> None:
     global config
     if not config["allow_send_to_admin"]:return
     if config["admin_group"] == 0:
          try:
               raise RuntimeWarning("未配置管理聊群QQ号，但是这被触发了，请配置admin_group。")
          except Exception:
               logger.warning(f"未配置管理聊群QQ号，但是这被触发了，\"{msg}\"将不会被发送！")
               exc_type,exc_vaule,exc_tb = sys.exc_info()
               logger.exception(f"{exc_type}:{exc_vaule}")

     bot:Bot = nonebot.get_bot()
     await bot.send_group_msg(group_id=config["admin_group"],message=msg)

debug = False


custom_menu = []

client = openai.AsyncOpenAI(base_url=config["open_ai_base_url"],api_key=config["open_ai_api_key"])
group_train = config["group_train"]
private_train = config["private_train"]
async def is_member(event: GroupMessageEvent,bot:Bot):
     user_role = await bot.get_group_member_info(group_id=event.group_id, user_id=event.user_id)
     user_role = user_role.get("role")
     if user_role == "member":return True
     return False
admins = config["admins"]

async def get_chat(messages:list)->str:
     completion = await client.chat.completions.create(model="auto", messages=messages,max_tokens=250,stream=True)
     response = ""
     async for chunk in completion:
                              try:
                                   response += chunk.choices[0].delta.content
                                   print(chunk.choices[0].delta.content)
                              except IndexError:
                                   break

     return response

#创建响应器实例
add_notice = on_notice(block=False)
menu = on_command("聊天菜单",block=True,aliases={"chat_menu"},priority=10)
chat = on_message(rule=to_me(),block=True,priority=11)
del_memory = on_command("del_memory",aliases={"失忆","删除记忆","删除历史消息","删除回忆"},block=True,priority=10)
enable = on_command("enable_chat",aliases={"启用聊天"},block=True,priority=10)
disable = on_command("disable_chat",aliases={"禁用聊天"},block=True,priority=10)
poke = on_notice(priority=10,block=True)
debug_switch = on_command("debug",priority=10,block=True)
debug_handle = on_message(rule=to_me(),priority=10,block=False)
recall = on_notice()
prompt = on_command("prompt",priority=10,block=True)



@prompt.handle()
async def _(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    """
    处理prompt命令的异步函数。此函数根据不同的条件和用户输入来管理prompt的设置和查询。
    
    参数:
    - bot: Bot对象，用于发送消息和与机器人交互。
    - event: GroupMessageEvent对象，包含事件的详细信息，如用户ID和消息内容。
    - args: Message对象，包含用户输入的命令参数。
    
    返回值:
    无返回值。
    """
    global config
    # 检查是否启用prompt功能，未启用则跳过处理
    if not config["enable"]:
        prompt.skip()
    # 检查是否允许自定义prompt，不允许则结束处理
    if not config["allow_custom_prompt"]:
        await prompt.finish("当前不允许自定义prompt。")
    
    global admins
    # 检查用户是否为群成员且非管理员，是则结束处理
    if await is_member(event, bot) and not event.user_id in admins:
        await prompt.finish("群成员不能设置prompt.")
        return
    
    data = get_memory_data(event)
    arg = args.extract_plain_text().strip()
    
    # 检查输入长度是否过长，过长则提示用户并返回
    if len(arg) >= 1000:
        await prompt.send("prompt过长，预期的参数不超过1000字。")
        return
    
    # 检查输入是否为空，为空则提示用户如何使用命令
    if arg.strip() == "":
        await prompt.send("请输入prompt或参数（--(show) 展示当前提示词，--(clear) 清空当前prompt，--(set) [文字]则设置提示词，e.g.:/prompt --(show)）,/prompt --(set) [text]。）")
        return
    
    # 根据用户输入的不同命令进行相应的处理
    if arg.startswith("--(show)"):
        await prompt.send(f"Prompt:\n{data.get('prompt','未设置prompt')}")
        return
    elif arg.startswith("--(clear)"):
        data["prompt"] = ""
        await prompt.send("prompt已清空。")
    elif arg.startswith("--(set)"):
        arg = arg.replace("--(set)","").strip()
        data["prompt"] = arg
        await prompt.send(f"prompt已设置为：\n{arg}")
    else:
        await prompt.send("请输入prompt或参数（--(show) 展示当前提示词，--(clear) 清空当前prompt，--(set) [文字]则设置提示词，e.g.:/prompt --(show)）,/prompt --(set) [text]。")
        return
    
    # 更新记忆数据
    write_memory_data(event, data)
               



# 当有人加入群聊时触发的事件处理函数
@add_notice.handle()
async def _(bot: Bot, event: GroupIncreaseNoticeEvent):
    """
    处理群聊增加通知事件的异步函数。
    
    参数:
    - bot: Bot对象，用于访问和操作机器人。
    - event: GroupIncreaseNoticeEvent对象，包含事件相关信息。
    
    此函数主要用于处理当机器人所在的群聊中增加新成员时的通知事件。
    它会根据全局配置变量config中的设置决定是否发送欢迎消息。
    """
    global config
    # 检查全局配置，如果未启用，则跳过处理
    if not config["enable"]:
        add_notice.skip()
    # 检查配置，如果不发送被邀请后的消息，则直接返回
    if not config["send_msg_after_be_invited"]:
        return
    # 如果事件的用户ID与机器人自身ID相同，表示机器人被邀请加入群聊
    if event.user_id == event.self_id:
        # 发送配置中的群聊添加消息
        await add_notice.send(config["group_added_msg"])
        return

# 处理调试模式开关的函数
@debug_switch.handle()
async def _ (bot:Bot,event:MessageEvent,matcher:Matcher):
    """
    根据用户权限开启或关闭调试模式。
    
    参数:
    - bot: Bot对象，用于调用API
    - event: 消息事件对象，包含消息相关信息
    - matcher: Matcher对象，用于控制事件处理流程
    
    返回值: 无
    """
    global admins,config
    # 如果配置中未启用调试模式，跳过后续处理
    if not config["enable"]:matcher.skip()
    # 如果不是管理员用户，直接返回
    if not event.user_id in admins:
        return
    global debug
    # 根据当前调试模式状态，开启或关闭调试模式，并发送通知
    if debug:
        debug = False
        await debug_switch.finish("已关闭调试模式（该模式适用于开发者，如果你作为普通用户使用，请关闭调试模式）")
    else:
        debug = True
        await debug_switch.finish("已开启调试模式（该模式适用于开发者，如果你作为普通用户使用，请关闭调试模式）")

# 处理调试信息的函数
@debug_handle.handle()
async def _(event:MessageEvent,bot:Bot,matcher:Matcher):
    """
    在调试模式下记录消息事件的相关信息，并处理用户消息。
    
    参数:
    - event: 消息事件对象，包含消息相关信息
    - bot: Bot对象，用于调用API
    - matcher: Matcher对象，用于控制事件处理流程
    
    返回值: 无
    """
    global debug,group_train,private_train,config
    # 如果配置中未启用调试模式，跳过后续处理
    if not config["enable"]:matcher.skip()
    # 如果调试模式未开启，直接返回
    if not debug:
        return
    # 获取群聊和私聊数据，并写入日志文件
    Group_Data = get_memory_data(event)
    with open ("debug_group_log.log",'w',encoding='utf-8') as fi:
            fi.write(str(Group_Data))
    Private_Data = get_memory_data(event)
    with open ("debug_private_log.log",'w',encoding='utf-8') as fi:
            fi.write(str(Private_Data))
    user_id = event.user_id
    content = ""
    # 根据事件类型处理消息，并记录到相应的日志文件
    if isinstance(event,GroupMessageEvent):
        types = ""
        types += "\nGroupMessageEvent"
        train = group_train
        for data in Group_Data:
            if data['id'] == event.group_id:
                break
        else:
            data = {False}
        with open (f"debug_group_{event.group_id}.log" ,'w',encoding='utf-8') as fi:
            fi.write(str(data.get("memory").get("messages")))
    else:
        train = private_train
        for data in Private_Data:
            if data['id'] == event.user_id:
                break
        else:
            data = {False}
        types = ""
        types += "\nPrivateMessageEvent"
        with open (f"debug_private_{event.user_id}.log" ,'w',encoding='utf-8') as fi:
            fi.write(str(data.get("memory").get("messages")))
    
    # 处理消息内容，根据消息类型记录相关信息
    for segment in event.get_message():
        if segment.type == "text":
            content = content + segment.data["text"]
        elif segment.type == "image":
            content += "\（图片：url='" +segment.data["url"].replace("https://multimedia.nt.qq.com.cn","https://micro-wave.cc:60017")+ "'）\\\n"
        elif segment.type == "json":
            content += "\（json：" +segment.data["data"]+ "）\\\n"
        elif segment.type == "node":
            content += "\（转发：" +str(segment.data["data"])+ "）\\\n"
        elif segment.type == "share":
            content += "\（分享：" +str(segment.data["url"])+ "）\\\n"
        elif segment.type =="xml":
            content += "\（xml：" +str(segment.data["data"])+ "）\\\n"
        elif segment.type == "at":
            content += f"\(at: @{segment.data['name']}(QQ:{segment.data['qq']}))"
        elif segment.type == "forward":
            forward = await bot.get_forward_msg(message_id=segment.data['id'])
            logger.debug(type(forward))
            content +="\（合并转发\n"+ await synthesize_forward_message(forward) + "）\\\n"
    
    # 处理引用的消息内容，并记录相关信息
    bot = nonebot.get_bot()
    reply = "（（（引用的消息）））：\n"
    if event.reply:
        dt_object = datetime.fromtimestamp(event.reply.time)  
        weekday = dt_object.strftime('%A')  
        formatted_time = dt_object.strftime('%Y-%m-%d %I:%M:%S %p') 
        DT = f"{formatted_time} {weekday}{event.reply.sender.nickname}（QQ:{event.reply.sender.user_id}）说：" 
        reply += DT
        for msg in event.reply.message:
            if msg.type == "text":
                reply += msg.data["text"]
            elif msg.type == "image":
                reply += "(图片：url='"+msg.data["url"].replace("https://multimedia.nt.qq.com.cn","https://micro-wave.cc:60017")+"'\\)\n"
            elif msg.type == "json":
                reply += "(json："+msg.data["data"]+")\n"
            elif msg.type == "node":
                reply += "(转发："+str(msg.data["data"])+")\n"
            elif msg.type == "share":
                reply += "(分享："+msg.data["url"]+")\n"
            elif msg.type =="xml":
                reply += "(xml："+msg.data["data"]+")\n"
            elif msg.type == "at":
                reply += f"\(at: @{msg.data['name']}(QQ:{msg.data['qq']}))"
            elif msg.type == "forward":
                forward = await bot.get_forward_msg(message_id=msg.data["id"])
                logger.debug(forward)
                reply +="\（合并转发\n"+ await synthesize_forward_message(forward) + "）\\\n"
    
    # 发送调试信息给管理员，并记录发送的消息内容
    await send_to_admin(f"{type} {user_id} {content}\nReply:{reply}\n{data}")
    sdmsg = data.get("memory").get("messages").copy()
    sdmsg.insert(0,train)
    await send_to_admin(f"SendMSG:\n{sdmsg[:500]}...")

# 当有消息撤回时触发处理函数
@recall.handle()
async def _(bot:Bot,event:GroupRecallNoticeEvent,matcher:Matcher):
    # 声明全局变量config，用于访问配置信息
    global config
    # 检查是否启用了插件功能，未启用则跳过后续处理
    if not config["enable"]:matcher.skip()
    # 通过随机数决定是否响应，增加趣味性和减少响应频率
    if not random.randint(1,3) == 2:
        return
    # 检查配置中是否允许在删除自己的消息后发言，不允许则直接返回
    if not config["say_after_self_msg_be_deleted"]:return
    # 从配置中获取删除消息后可能的回复内容
    recallmsg = config["after_deleted_say_what"]
    # 判断事件是否为机器人自己删除了自己的消息
    if event.user_id == event.self_id:
        # 如果是机器人自己删除了自己的消息，并且操作者也是机器人自己，则不进行回复
        if event.operator_id == event.self_id:
            return
        # 从预设的回复内容中随机选择一条发送
        await recall.send(random.choice(recallmsg))
        return





# 定义聊天功能菜单的初始消息内容，包含各种命令及其描述
menu_msg = "聊天功能菜单:\n/聊天菜单 唤出菜单 \n/del_memory 丢失这个群/聊天的记忆 \n/enable 在群聊启用聊天 \n/disable 在群聊里关闭聊天\n/prompt <arg> [text] 设置聊群自定义补充prompt（--(show) 展示当前提示词，--(clear) 清空当前prompt，--(set) [文字]则设置提示词，e.g.:/prompt --(show)）,/prompt --(set) [text]。）"

# 处理菜单命令的函数
@menu.handle()
async def _(event:MessageEvent,matcher:Matcher):
    # 声明全局变量，用于访问和修改自定义菜单、默认菜单消息以及配置信息
    global custom_menu,menu_msg,config
    
    # 检查聊天功能是否已启用，未启用则跳过处理
    if not config["enable"]:
        matcher.skip()
    
    # 初始化消息内容为默认菜单消息
    msg = menu_msg
    
    # 遍历自定义菜单项，添加到消息内容中
    for menu in custom_menu:
        msg += f"\n{menu['cmd']} {menu['describe']}"
    
    # 根据配置信息，添加群聊或私聊聊天可用性的提示信息
    msg += f"\n{'群内可以at我与我聊天，' if config['enable_group_chat'] else '未启用群内聊天，'}{'在私聊可以直接聊天。' if config['enable_private_chat'] else '未启用私聊聊天'}\nPowered by Suggar chat plugin"
    
    # 发送最终的消息内容
    await menu.send(msg)

@poke.handle()
async def _(event:PokeNotifyEvent,bot:Bot,matcher:Matcher):
    """
    处理戳一戳事件的异步函数。
    
    参数:
    - event: 戳一戳通知事件对象。
    - bot: 机器人对象。
    - matcher: 匹配器对象，用于控制事件处理流程。
    
    此函数主要根据配置信息和事件类型，响应戳一戳事件，并发送预定义的消息。
    """
    # 声明全局变量，用于获取prompt和调试模式
    global private_train,group_train
    global debug,config
    
    # 检查配置，如果机器人未启用，则跳过处理
    if not config["enable"]:
        matcher.skip()
    
    # 如果配置中未开启戳一戳回复，则直接返回
    if not config["poke_reply"]:
        poke.skip()
        return
    
    # 获取群聊和私聊的数据
    Group_Data = get_memory_data(event)
    Private_Data = get_memory_data(event)
    
    # 如果事件的目标ID不是机器人自身，则直接返回
    if event.target_id != event.self_id:
        return

    try:
        # 判断事件是否发生在群聊中
        if event.group_id != None:
            i = Group_Data
            # 如果群聊ID匹配且群聊功能开启，则处理事件
            if i['id'] == event.group_id and i['enable']:
                # 获取用户昵称
                user_name = (await bot.get_group_member_info(group_id=event.group_id, user_id=event.user_id))['nickname'] or (await bot.get_stranger_info(user_id=event.user_id))['nickname']
                # 构建发送的消息内容
                send_messages = [
                    {"role": "system", "content": f"{group_train}"},
                    {"role": "user", "content": f"\(戳一戳消息\){user_name} (QQ:{event.user_id}) 戳了戳你"}
                ]
                
                # 初始化响应内容和调试信息
                response = ""
                debug_response = []
                
                # 创建聊天完成对象
                completion = await client.chat.completions.create(model="auto", messages=send_messages,max_tokens=250,stream=True) 
                
                # 异步处理聊天响应
                async for chunk in completion:
                    try:
                        response += chunk.choices[0].delta.content
                        print(chunk.choices[0].delta.content)
                    except IndexError:
                        break
                debug_response.append(response)
                
                # 如果调试模式开启，发送调试信息给管理员
                if debug:
                    await send_to_admin(f"POKEMSG{event.group_id}/{event.user_id}\n {send_messages}") 
                    await send_to_admin(f"RESPONSE:\n{completion},raw:\n{debug_response}")
                
                # 构建最终消息并发送
                message = MessageSegment.at(user_id=event.user_id) +" "+ MessageSegment.text(response)
                i['memory']['messages'].append({"role":"assistant","content":str(response)})
                
                # 更新群聊数据
                write_memory_data(event,i)
                await poke.send(message)
        
        else:
            # 如果事件发生在私聊中，执行类似的处理流程
            i = Private_Data
            if i['id'] == event.user_id and i['enable']:
                name = get_friend_info(event.user_id)
                send_messages = [
                    {"role": "system", "content": f"{private_train}"},
                    {"role": "user", "content": f" \(戳一戳消息\) {name}(QQ:{event.user_id}) 戳了戳你"}
                ]
                
                completion = await client.chat.completions.create(model="auto", messages=send_messages,max_tokens=250,stream=True)
                response = ""
                debug_response = []        
                print(type(completion))
                
                async for chunk in completion:
                    try:
                        response += chunk.choices[0].delta.content
                        print(chunk.choices[0].delta.content)
                    except IndexError:
                        break
                    debug_response.append(chunk)
                
                if debug:
                    await send_to_admin(f"POKEMSG {send_messages}") 
                    await send_to_admin(f"RESPONSE:\n{completion}\nraw:{debug_response}")
                
                message = MessageSegment.text(response)
                i['memory']['messages'].append({"role":"assistant","content":str(response)})
                write_memory_data(event,i)
                await poke.send(message)
                
    except Exception as e:
        # 异常处理，记录错误信息并发送给管理员
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logger.error(f"Exception type: {exc_type.__name__}")  
        logger.error(f"Exception message: {str(exc_value)}")  
        import traceback  
        await send_to_admin(f"出错了！{exc_value},\n{str(exc_type)}")
        await send_to_admin(f"{traceback.format_exc()}")
        
        if isinstance(e,AttributeError):
            await send_to_admin(f"{completion}")
        
        try:
            if debug:
                warn = completion
                await send_to_admin(f"ERROR:{warn}")
        except:
            logger.error("无法的得到接口返回报错信息！")
            await send_to_admin(f"无法的得到接口返回报错信息！")
        
        logger.error(f"Detailed exception info:\n{''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))}")       



@disable.handle()
async def _(bot: Bot, event: GroupMessageEvent, matcher: Matcher):
    """
    处理禁用聊天功能的异步函数。
    
    当接收到群消息事件时，检查当前配置是否允许执行禁用操作，如果不允许则跳过处理。
    检查发送消息的成员是否为普通成员且不在管理员列表中，如果是则发送提示消息并返回。
    如果成员有权限，记录日志并更新记忆中的数据结构以禁用聊天功能，然后发送确认消息。
    
    参数:
    - bot: Bot对象，用于调用机器人API。
    - event: GroupMessageEvent对象，包含群消息事件的相关信息。
    - matcher: Matcher对象，用于控制事件处理流程。
    
    返回: 无
    """
    global admins, config
    # 检查全局配置是否启用，如果未启用则跳过后续处理
    if not config["enable"]:
        matcher.skip()
    
    # 获取发送消息的成员信息
    member = await bot.get_group_member_info(group_id=event.group_id, user_id=event.user_id)
    
    # 检查成员是否为普通成员且不在管理员列表中，如果是则发送提示消息并返回
    if member["role"] == "member" and event.user_id not in admins:
        await disable.send("你没有这样的力量呢～（管理员/管理员+）")
        return
    
    # 记录禁用操作的日志
    logger.debug(f"{event.group_id} disabled")
    
    # 获取并更新记忆中的数据结构
    datag = get_memory_data(event)
    if True:
        if datag["id"] == event.group_id:
            if not datag['enable']:
                await disable.send("聊天禁用")
            else:
                datag['enable'] = False
                await disable.send("聊天已经禁用")
    
    # 将更新后的数据结构写回记忆
    write_memory_data(event, datag)

@enable.handle()
async def _(bot: Bot, event: GroupMessageEvent, matcher: Matcher):
    """
    处理启用聊天功能的命令。

    该函数检查当前配置是否允许启用聊天功能，如果允许则检查发送命令的用户是否为管理员。
    如果用户是普通成员且不在管理员列表中，则发送提示信息并返回。
    如果用户有权限，且当前聊天功能已启用，则发送“聊天启用”的消息。
    如果聊天功能未启用，则启用聊天功能并发送“聊天启用”的消息。

    参数:
    - bot: Bot对象，用于调用API。
    - event: GroupMessageEvent对象，包含事件相关的信息。
    - matcher: Matcher对象，用于控制事件的处理流程。
    """
    global admins, config
    # 检查全局配置，如果未启用则跳过后续处理
    if not config["enable"]:
        matcher.skip()

    # 获取发送命令的用户在群中的角色信息
    member = await bot.get_group_member_info(group_id=event.group_id, user_id=event.user_id)
    # 如果用户是普通成员且不在管理员列表中，则发送提示信息并返回
    if member["role"] == "member" and event.user_id not in admins:
        await enable.send("你没有这样的力量呢～（管理员/管理员+）")
        return

    # 记录日志
    logger.debug(f"{event.group_id}enabled")
    # 获取记忆中的数据
    datag = get_memory_data(event)
    # 检查记忆数据是否与当前群组相关
    if True:
        if datag["id"] == event.group_id:
            # 如果聊天功能已启用，则发送提示信息
            if datag['enable']:
                await enable.send("聊天启用")
            else:
                # 如果聊天功能未启用，则启用并发送提示信息
                datag['enable'] = True
                await enable.send("聊天启用")
    # 更新记忆数据
    write_memory_data(event, datag)

   
@del_memory.handle()
async def _(bot:Bot,event:MessageEvent,matcher:Matcher):
    
    global admins,config
    if not config["enable"]:matcher.skip()
    if isinstance(event,GroupMessageEvent):
        member = await bot.get_group_member_info(group_id=event.group_id,user_id=event.user_id)
        
        
        if  member["role"] == "member" and not event.user_id in admins:
                await del_memory.send("你没有这样的力量（管理员/管理员+）")
                return
        GData = get_memory_data(event)
        if True:
            if GData["id"] == event.group_id:
                GData['memory']['messages'] = []
                await del_memory.send("上下文已清除")
                write_memory_data(event,GData)
                logger.debug(f"{event.group_id}Memory deleted")
                
                
      
    else:
            FData = get_memory_data(event)
            if FData["id"] == event.user_id:
                FData["memory"]["messages"] = []
                await del_memory.send("上下文已清除")
                logger.debug(f"{event.user_id}Memory deleted")
                write_memory_data(event,FData)
       
          
@get_driver().on_startup
async def Startup():
    memory_private = []
    memory_group = []
    from .conf import group_memory,private_memory
    from pathlib import Path
    if not Path(group_memory).exists() and not Path(group_memory).is_dir():
        Path.mkdir(group_memory)
    if not Path(private_memory).exists() and not Path(private_memory).is_dir():
        Path.mkdir(private_memory)
    logger.info("启动成功")


@chat.handle()
async def _(event:MessageEvent,matcher:Matcher,bot:Bot):
    global debug,config
    if not config["enable"]:matcher.skip()
    memory_lenth_limit = config["memory_lenth_limit"]
 

    Date = get_current_datetime_timestamp()
    bot = nonebot.get_bot()
    global group_train,private_train
    
    content = ""
    logger.info(event.get_message())
    if event.message.extract_plain_text().strip().startswith("/"):
         matcher.skip()
         return

    if event.message.extract_plain_text().startswith("菜单"):
         await matcher.finish(menu_msg)
         return
    dataDir =os.path.dirname(os.path.abspath(__file__))+ "\speak_module"
    savePath = os.path.join(dataDir, "res", f"temp{random.randint(1,1023)}.mp3")
    logger.debug (savePath)
    Group_Data = get_memory_data(event)
    Private_Data = get_memory_data(event)

        
    if event.get_message():
     try:
        if isinstance(event,GroupMessageEvent):
            
                datag = Group_Data
                if datag["id"] == event.group_id:
                    if not datag["enable"]:
                        await chat.send( "聊天没有启用，快去找管理员吧！")
                        chat.skip()
                        return
                    
                    group_id = event.group_id
                    user_id = event.user_id
                    content = ""
                    user_name = (await bot.get_group_member_info(group_id=group_id, user_id=user_id))['card'] or (await bot.get_stranger_info(user_id=user_id))['nickname']
                    for segment in event.get_message():
                        if segment.type == "text":
                            content = content + segment.data["text"]

                        elif segment.type == "at":
                             content += f"\(at: @{segment.data['name']}(QQ:{segment.data['qq']}))"
                        elif segment.type == "forward":
                            
                            forward = await bot.get_forward_msg(message_id=segment.data['id'])
                            logger.debug(forward)
                            content +="\（合并转发\n"+ await synthesize_forward_message(forward) + "）\\\n"
                    if content.strip() == "":
                         content = ""
                    role = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
                    
                    if role['role'] == "admin":
                         role = "群管理员"
                    elif role['role'] == "owner":
                         role = "群主"
                    elif role['role'] == "member":
                         role = "普通成员"
                    logger.debug(f"{Date}{user_name}（{user_id}）说:{content}")
                    reply = "（（（引用的消息）））：\n"
                    if event.reply:
                         dt_object = datetime.fromtimestamp(event.reply.time)  
                         weekday = dt_object.strftime('%A')  
                        # 格式化输出结果  
                         try:
                          rl = await bot.get_group_member_info(group_id=group_id, user_id=event.reply.sender.user_id)
                          
                          if rl['rl'] == "admin":
                            rl = "群管理员"
                          elif rl['rl'] == "owner":
                            rl = "群主"
                          elif rl['rl'] == "member":
                            rl = "普通成员"
                          elif event.reply.sender.user_id==event.self_id:
                            rl = "自己"
                         except:
                            if event.reply.sender.user_id==event.self_id:
                                rl = "自己"
                            else:
                                rl = "[获取身份失败]"
                         formatted_time = dt_object.strftime('%Y-%m-%d %I:%M:%S %p') 
                         DT = f"{formatted_time} {weekday} [{rl}]{event.reply.sender.nickname}（QQ:{event.reply.sender.user_id}）说：" 
                         reply += DT
                         for msg in event.reply.message:
                             if msg.type == "text":
                                  reply += msg.data["text"]
        
                             elif msg.type == "at":
                                 reply += f"\(at: @{msg.data['name']}(QQ:{msg.data['qq']}))\\"
                             elif msg.type == "forward":
                                
                                forward = await bot.get_forward_msg(message_id=msg.data["id"])
                                logger.debug(forward)
                                reply +="\（合并转发\n"+ await synthesize_forward_message(forward) + "）\\\n"
                             elif msg.type == "markdown":
                                  reply += "\\(Markdown消息 暂不支持)\\"
                         content += str(reply)
                         logger.debug(reply)
                         logger.debug(f"[{role}][{Date}][{user_name}（{user_id}）]说:{content}")
    
                    datag["memory"]["messages"].append({"role":"user","content":f"[{role}][{Date}][{user_name}（{user_id}）]说:{content}"})
                    if len(datag["memory"]["messages"]) >memory_lenth_limit:
                        while len(datag["memory"]["messages"])>memory_lenth_limit:
                            del datag["memory"]["messages"][0]
                    send_messages = []
                    send_messages = datag["memory"]['messages'].copy()
                    group_train = resources.group_train.copy()
                    train = group_train.copy()
                    
                    train["content"] += f"\n以下是一些补充内容，如果与上面任何一条有冲突请忽略。\n{datag.get('prompt','无')}"
                    send_messages.insert(0,train)
                    try:    
                            
                            completion = await client.chat.completions.create(model="auto", messages=send_messages,max_tokens=250,stream=True)
                            response = ""
                            debug_response = []
                            
                            async for chunk in completion:
                              try:
                                   response += chunk.choices[0].delta.content
                                   print(chunk.choices[0].delta.content)
                              except IndexError:
                                   break
                              debug_response .append(chunk)
   
                            message = MessageSegment.at(user_id=user_id) + MessageSegment.text(response) 
                           
                            if debug:
                                 await send_to_admin(f"{event.group_id}/{event.user_id}\n{event.message.extract_plain_text()}\n{type(event)}\nRESPONSE:\n{str(response)}\nraw:{debug_response}")
                            if debug:
                                 logger.debug(datag["memory"]["messages"])
                                 logger.debug(str(response))
                                 await send_to_admin(f"response:{response}")
                                 
                            datag["memory"]["messages"].append({"role":"assistant","content":str(response)})
                   
                            await chat.send(message)
                    
                    except Exception as e:
                        await chat.send(f"Suggar出错了呢～稍后试试吧～（错误已反馈") 
                        
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        logger.error(f"Exception type: {exc_type.__name__}")  
                        logger.error(f"Exception message: {str(exc_value)}")  
                        import traceback  
                        await send_to_admin(f"出错了！{exc_value},\n{str(exc_type)}")
                        await send_to_admin(f"{traceback.format_exc()}")
                        if isinstance(e,AttributeError):
                             await send_to_admin(f"{completion}")
                        try:
                             if debug:
                                warn = completion
                                await send_to_admin(f"ERROR:{warn}")
                        except:
                            logger.error("无法的得到接口返回报错信息！")
                            await send_to_admin(f"无法的得到接口返回报错信息！")
                        logger.error(f"Detailed exception info:\n{''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))}")      
 
            
                    write_memory_data(event,datag) 
        else:
         
                data = Private_Data
                if data["id"] == event.user_id:
                    content = ""
                    rl = ""
                    for segment in event.get_message():
                        if segment.type == "text":
                            content = content + segment.data["text"]

                        elif segment.type == "at":
                             content += f"\(at: @{segment.data['name']}(QQ:{segment.data['qq']}))"
                        elif segment.type == "forward":
                            logger.debug(segment)
                            forward = await bot.get_forward_msg(message_id=segment.data["id"])
                            logger.debug(type(forward))
                            content+="\（合并转发\n"+ await synthesize_forward_message(forward) + "）\\\n"
                    if content.strip() == "":
                         content = ""
                    logger.debug(f"{content}")
                    reply = "（（（引用的消息）））：\n"
                    if event.reply:
                         dt_object = datetime.fromtimestamp(event.reply.time)  
                         weekday = dt_object.strftime('%A')  
                        # 格式化输出结果  
                         
                         formatted_time = dt_object.strftime('%Y-%m-%d %I:%M:%S %p') 
                         DT = f"{formatted_time} {weekday} {rl} {event.reply.sender.nickname}（QQ:{event.reply.sender.user_id}）说：" 
                         reply += DT
                         for msg in event.reply.message:
                             if msg.type == "text":
                                  reply += msg.data["text"]
              
                             elif segment.type == "at":
                                reply += f"\(at: @{msg.data['name']}(QQ:{msg.data['qq']}))"
                             elif msg.type == "forward":
                              
                                forward = await bot.get_forward_msg(message_id=msg.data["id"])
                                logger.debug(type(forward))
                                reply +="\（合并转发\n"+ await synthesize_forward_message(forward) + "）\\\n"
                         content += str(reply)
                         logger.debug(reply)
                     
                    data["memory"]["messages"].append({"role":"user","content":f"{Date}{await get_friend_info(event.user_id)}（{event.user_id}）： {str(content)}"})
                    if len(data["memory"]["messages"]) >memory_lenth_limit:
                        while len(data["memory"]["messages"])>memory_lenth_limit:
                            del data["memory"]["messages"][0]
                    send_messages = []
                    send_messages = data["memory"]["messages"].copy()
                    send_messages.insert(0,private_train)
                    try:    
                            response = ""
                            completion = await client.chat.completions.create(model="auto", messages=send_messages,max_tokens=250,stream=True)
                            
                            
                            async for chunk in completion:
                              try:
                                   response += chunk.choices[0].delta.content
                                   print(chunk.choices[0].delta.content)
                              except IndexError:
                                   break
                              debug_response = []
                            
                              debug_response .append(chunk)

           
                            if debug:
                                 if debug:
                                    await send_to_admin(f"{event.user_id}\n{type(event)}\n{event.message.extract_plain_text()}\nRESPONSE:\n{str(response)}\nraw:{debug_response}")
                            message =  MessageSegment.text(response)
                            
                            
                            
                            if debug:
                                 logger.debug(data["memory"]["messages"])
                                 logger.debug(str(response))
               
                                 await send_to_admin(f"response:{response}")
                                 
                            data["memory"]["messages"].append({"role":"assistant","content":str(response)})
                          
                            await chat.send(message)
                           
                            
                                
                    except Exception as e:
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        await chat.send(f"Suggar出错了呢～稍后试试吧～（错误已反馈")
                        logger.error(f"Exception type: {exc_type.__name__}")  
                        logger.error(f"Exception message: {str(exc_value)}")  
                        import traceback  
                        await send_to_admin(f"出错了！{exc_value},\n{str(exc_type)}")
                        await send_to_admin(f"{traceback.format_exc()} ")
                        if isinstance(e,AttributeError):
                             await send_to_admin(f"{completion}")
                        try:
                             if debug:
                                warn = completion
                                await send_to_admin(f"ERROR:{warn}")
                        except:
                             logger.error("无法的得到接口返回报错信息！")
                             await send_to_admin(f"无法的得到接口返回报错信息！")
                        logger.error(f"Detailed exception info:\n{''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))}")      
              
                        write_memory_data(event,data)      
     except Exception as e:
                        await chat.send(f"Suggar出错了呢～稍后试试吧～（错误已反馈 ") 
                        
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        logger.error(f"Exception type: {exc_type.__name__}")  
                        logger.error(f"Exception message: {str(exc_value)}")  
                        import traceback  
                        await send_to_admin(f"出错了！{exc_value},\n{str(exc_type)}")
                        await send_to_admin(f"{traceback.format_exc()}")
                        if isinstance(e,AttributeError):
                             await send_to_admin(f"{completion}")
                        try:
                             if debug:
                                warn = completion
                                await send_to_admin(f"ERROR:{warn}")
                        except:
                             logger.error("无法的得到接口返回报错信息！")
                             await send_to_admin(f"无法的得到接口返回报错信息！")
                        logger.error(f"Detailed exception info:\n{''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))}")    
    else:pass
    write_memory_data(event,data)
    