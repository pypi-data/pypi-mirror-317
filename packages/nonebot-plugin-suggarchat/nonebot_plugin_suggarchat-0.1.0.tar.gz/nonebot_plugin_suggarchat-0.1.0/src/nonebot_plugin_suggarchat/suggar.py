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

config = resources.__default_config__
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




client = openai.AsyncOpenAI(base_url=config["open_ai_base_url"],api_key=config["open_ai_api_key"])
group_train = config["group_train"]
private_train = config["private_train"]
async def is_member(event: GroupMessageEvent,bot:Bot):
     user_role = await bot.get_group_member_info(group_id=event.group_id, user_id=event.user_id)
     user_role = user_role.get("role")
     if user_role == "member":return True
     return False
admins = config["admins"]

def read_list_from_yaml(file_path:str)->list:  
  try:
    with open(file_path, 'r', encoding='utf-8') as file:  
        data = yaml.safe_load(file)  
  except FileNotFoundError:
    with open(file_path, 'w', encoding='utf-8') as file:  
        data = {'users': []}  
        yaml.dump(data, file)
  return data['users'] 
def write_list_to_yaml(file_path:str, fruits_list:list)->None:  
    with open(file_path, 'w', encoding='utf-8') as file:  
        yaml.dump({'users': fruits_list}, file, default_flow_style=False, allow_unicode=True) 
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

add_notice = on_notice(block=False)
menu = on_command("聊天菜单",block=True,aliases={"chat_menu"},priority=10)

chat = on_message(rule=to_me(),block=True,priority=11)
del_memory = on_command("del_memory",aliases={"失忆","删除记忆","删除历史消息","删除回忆"},block=True,priority=10)
enable = on_command("enable_chat",aliases={"启用聊天"},block=True,priority=10)
disable = on_command("disable_chat",aliases={"禁用聊天"},block=True,priority=10)

poke = on_notice(priority=10,block=True)



debug_switch = on_command("debug",priority=10,block=True)
debug_handle = on_message(rule=to_me(),priority=10,block=False)


full_mode = on_command("full_mode",priority=10,block=True)

recall = on_notice()
prompt = on_command("prompt",priority=10,block=True)


admin_menu = on_command("admin",priority=1,block=True)


@prompt.handle()
async def _(bot: Bot, event: GroupMessageEvent,args: Message = CommandArg()):
     global config
     if not config["allow_custom_prompt"]:await prompt.finish("当前不允许自定义prompt。")
     global admins
     if await is_member(event,bot) and not event.user_id in admins:
          await prompt.finish("群成员不能设置prompt.")
          return
     data = get_memory_data(event)
     arg = args.extract_plain_text().strip()
   
     if len(arg) >= 1000:
          await prompt.send("prompt过长，预期的参数不超过1000字。")
          return
     
     if arg.strip() == "":
          await prompt.send("请输入prompt或参数（--(show) 展示当前提示词，--(clear) 清空当前prompt，--(set) [文字]则设置提示词，e.g.:/prompt --(show)）,/prompt --(set) [text]。）")
          return
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



     write_memory_data(event,data)
               


@admin_menu.handle()
async def _(bot:Bot,event:MessageEvent):
     global admins
     if not event.user_id in admins:
          await admin_menu.finish("你无法调出菜单。")
          return
     await admin_menu.send("/set(user_id:int Object:str) -> str\n/ban-user(user_id:int) -> str\n/ban-group(group_id:int) -> str\n/pardon-user(user_id:int) -> str\n/pardon-group(group_id:int) -> str\n/debug\n/fixing(reason:str) -> str\n/list() -> str\nself.get_command()-> /admin")

@add_notice.handle()
async def _(bot:Bot,event:GroupIncreaseNoticeEvent):
     global config
     if not config["send_msg_after_be_invited"]:return
     if event.user_id == event.self_id:
          await add_notice.send(config["group_added_msg"])
          return

     



@full_mode.handle()
async def _(bot:Bot,event:MessageEvent,matcher:Matcher):
     Group_Data = get_memory_data(event)
     Private_Data = get_memory_data(event)
     if isinstance(event,GroupMessageEvent):
          data = Group_Data
     
     else:data = Private_Data
     i = data
     if data == data:
               if i['id'] == event.group_id:
                    if i.get("full") !=None:
                         if not i['full']:
                              i['full'] = True
                              await full_mode.send("已开启反接口和谐模式")
                              
                         else:
                              i['full'] = False
                              await full_mode.send("已关闭反接口和谐模式")
                              
                    else:
                         i['full'] = True
                         await full_mode.send("已开启反接口和谐模式")
                         
     else:
               await full_mode.send("请开始聊天后再尝试设置。")
     write_memory_data(event,data)



@debug_switch.handle()
async def _ (bot:Bot,event:MessageEvent):
     global admins
     if not event.user_id in admins:
          return
     global debug
     if debug:
          debug = False
          await debug_switch.finish("已关闭调试模式（该模式适用于开发者，如果你作为普通用户使用，请关闭调试模式）")
     else:
          debug = True
          await debug_switch.finish("已开启调试模式（该模式适用于开发者，如果你作为普通用户使用，请关闭调试模式）")

@debug_handle.handle()
async def _(event:MessageEvent,bot:Bot):
    global debug,group_train,private_train
    if not debug:
          return
    Group_Data = get_memory_data(event)
    with open ("debug_group_log.log",'w',encoding='utf-8') as fi:
            fi.write(str(Group_Data))
    Private_Data = get_memory_data(event)
    with open ("debug_private_log.log",'w',encoding='utf-8') as fi:
            fi.write(str(Private_Data))
    user_id = event.user_id
    content = ""
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
    await send_to_admin(f"{type} {user_id} {content}\nReply:{reply}\n{data}")
    sdmsg = data.get("memory").get("messages").copy()
    sdmsg.insert(0,train)
    
    await send_to_admin(f"SendMSG:\n{sdmsg[:500]}...")
          

@recall.handle()
async def _(bot:Bot,event:GroupRecallNoticeEvent):
     global config
     if not random.randint(1,3) == 2:
          return
     if not config["say_after_self_msg_be_deleted"]:return
     recallmsg = config["after_deleted_say_what"]
     if event.user_id == event.self_id:
          if event.operator_id == event.self_id:
               return
          await recall.send(random.choice(recallmsg))
          return





menu_msg = "聊天功能菜单:\n/聊天菜单 唤出菜单 \n/del_memory 丢失这个群/聊天的记忆 \n/enable 在群聊启用聊天 \n/disable 在群聊里关闭聊天\n/prompt <arg> [text] 设置聊群自定义补充prompt（--(show) 展示当前提示词，--(clear) 清空当前prompt，--(set) [文字]则设置提示词，e.g.:/prompt --(show)）,/prompt --(set) [text]。）\n群内可以at我与我聊天，在私聊可以直接聊天。Powered by Suggar chat plugin"
@menu.handle()
async def _(event:MessageEvent):
    await menu.send(menu_msg)


@poke.handle()
async def _(event:PokeNotifyEvent,bot:Bot,matcher:Matcher):
    
    global private_train,group_train
    global debug,config
    if not config["poke_reply"]:
         poke.skip()
         return
    Group_Data = get_memory_data(event)
    Private_Data = get_memory_data(event)
    if event.target_id != event.self_id:return

    try:
     if event.group_id != None:
        
         
              i = Group_Data
              if i['id'] == event.group_id and i['enable']:
                   user_name = (await bot.get_group_member_info(group_id=event.group_id, user_id=event.user_id))['nickname'] or (await bot.get_stranger_info(user_id=event.user_id))['nickname']
                   send_messages = [
                       {"role": "system", "content": f"{group_train}"},
                       {"role": "user", "content": f"\(戳一戳消息\){user_name} (QQ:{event.user_id}) 戳了戳你"}
                   ]
                   
                   response = ""
                   debug_response = []
                            
                   completion = await client.chat.completions.create(model="auto", messages=send_messages,max_tokens=250,stream=True) 
                 
                   async for chunk in completion:
                              try:
                                   response += chunk.choices[0].delta.content
                                   print(chunk.choices[0].delta.content)
                              except IndexError:
                                   break
                   debug_response .append(response)
                   if debug:
                        await send_to_admin(f"POKEMSG{event.group_id}/{event.user_id}\n {send_messages}") 
                        await send_to_admin(f"RESPONSE:\n{completion},raw:\n{debug_response}")
                   
                   message = MessageSegment.at(user_id=event.user_id) +" "+ MessageSegment.text(response)
                   i['memory']['messages'].append({"role":"assistant","content":str(response)})
                   
                   write_memory_data(event,i)
                   await poke.send(message)
             
                   
    
        
     else:
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
                              debug_response .append(chunk)
                   if debug:
                        await send_to_admin(f"POKEMSG {send_messages}") 
                        await send_to_admin(f"RESPONSE:\n{completion}\nraw:{debug_response}")
                   message = MessageSegment.text(response)
                   i['memory']['messages'].append({"role":"assistant","content":str(response)})
                   write_memory_data(event,i)
                   await poke.send(message)
               
    except Exception as e:
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
async def _(bot:Bot,event:GroupMessageEvent):
    global admins
    member = await bot.get_group_member_info(group_id=event.group_id,user_id=event.user_id)
    if  member["role"] == "member" and event.user_id not in admins:
                await disable.send("你没有这样的力量呢～（管理员/管理员+）")
                return
    logger.debug(f"{event.group_id}disabled")
    datag = get_memory_data(event)
    if True:
        if datag["id"] == event.group_id :
            if not datag['enable']:
                await disable.send("聊天禁用")
                
            else:
                datag['enable'] = False
                await disable.send("聊天已经禁用")
               
    write_memory_data(event,datag)

@enable.handle()
async def _(bot:Bot,event:GroupMessageEvent):
    global admins
    member = await bot.get_group_member_info(group_id=event.group_id,user_id=event.user_id)
    if  member["role"] == "member" and event.user_id not in admins:
                await enable.send("你没有这样的力量呢～（管理员/管理员+）")
                return
    logger.debug(f"{event.group_id}enabled")
    datag = get_memory_data(event)
    if True:
                
                if datag["id"] == event.group_id :
                    if datag['enable']:
                        await enable.send("聊天启用")
                        
                    else:
                        datag['enable'] = True
                        await enable.send("聊天启用")
    write_memory_data(event,datag)



   
@del_memory.handle()
async def _(bot:Bot,event:MessageEvent):
    
    global admins
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
   # model = "@cf/qwen/qwen1.5-14b-chat-awq"
    #model = "@cf/google/gemma-7b-it-lora"
    
        
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
    