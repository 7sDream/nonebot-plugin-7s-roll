import re
from asyncio import create_task

import nonebot
from nonebot.adapters.cqhttp import Bot

from .config import Config

DRIVER = G_CONF = SEP = START = CONF = None
try:
    DRIVER = nonebot.get_driver()
    G_CONF = DRIVER.config
    START = next(iter(G_CONF.command_start))
    SEP = next(iter(G_CONF.command_sep))
    CONF = Config(**G_CONF.dict())
except ValueError:
    pass
