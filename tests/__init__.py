import nonebot
from nonebot.adapters.console import Adapter

nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter(Adapter)
nonebot.load_builtin_plugins()
nonebot.load_plugin("nonebot_plugin_7s_roll")
