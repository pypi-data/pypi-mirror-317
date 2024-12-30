
from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from .conf import __KERNEL_VERSION__
from .config import Config
from .conf import *
from .resources import *
from .suggar import *
from .API import *

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_suggarchat",
    description="Plugin for the Suggar chat framework compatible with Nonebot2.",
    usage="按照Readme.md修改配置文件后使用。",
    config=Config,
    homepage="https://github.com/JohnRichard4096/nonebot_plugin_suggarchat/",
    type="application",
    supported_adapters={"~onebot.v11"}
)

config = get_plugin_config(Config)




