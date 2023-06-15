import re
from asyncio import create_task

import nonebot

from .config import Config

DRIVER = nonebot.get_driver()
G_CONF = DRIVER.config
START = next(iter(G_CONF.command_start))
CONF = Config(**G_CONF.dict())
