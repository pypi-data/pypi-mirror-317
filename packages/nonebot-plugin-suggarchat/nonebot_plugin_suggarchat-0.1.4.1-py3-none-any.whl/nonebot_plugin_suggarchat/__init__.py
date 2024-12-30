
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
    usage="use OpenAI API to chat",
    config=Config,
    homepage="https://github.com/JohnRichard4096/nonebot_plugin_suggarchat/",
    type="application",
    author="JohnRichard4096",
    version=__KERNEL_VERSION__,
    supported_adapters={"~onebot.v11"}
)

config = get_plugin_config(Config)




