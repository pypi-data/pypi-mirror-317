from nonebot import logger
from .conf import *

from .conf import __KERNEL_VERSION__
from .resources import *
from .suggar import *


logger.info(f"""
NONEBOT PLUGIN SUGGARCHAT
{__KERNEL_VERSION__}
""")
# 打印当前工作目录  
logger.info("当前工作目录:"+ current_directory)
logger.info(f"配置文件目录：{config_dir}") 
logger.info(f"主配置文件：{main_config}")
logger.info(f"群记忆文件目录：{group_memory}")
logger.info(f"私聊记忆文件目录：{private_memory}")

