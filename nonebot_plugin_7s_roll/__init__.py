from .command import cmd_roll, message_cmd_roll
from .config import Config
from .roll import roll

__version__ = "0.2.0a2"

from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name = "7sRoll",
    description="roll 点工具",
    usage="/roll 3d10",
    config = Config,
    extra={},
)
