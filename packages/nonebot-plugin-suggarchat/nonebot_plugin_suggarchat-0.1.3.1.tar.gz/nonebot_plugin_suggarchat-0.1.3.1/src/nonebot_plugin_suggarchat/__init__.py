
from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from .conf import __KERNEL_VERSION__
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_suggarchat",
    description="Plugin for the Suggar chat framework compatible with Nonebot2.",
    usage="use OpenAI API to chat",
    config=Config,
    homepage="https://github.com/JohnRichard4096/nonebot_plugin_suggarchat/",
    type="application",
    author="JohnRichard4096",
    version=__KERNEL_VERSION__,
)

config = get_plugin_config(Config)


from .conf import *
from nonebot import logger

from .resources import *
from .suggar import *
from .API import *
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
logger.info(f"当前配置文件：{get_config()}")

