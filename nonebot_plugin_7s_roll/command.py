import re
from typing import Annotated

import nonebot.adapters.onebot.v11 as onebot11
from nonebot import on_command, on_message
from nonebot.adapters import Event
from nonebot.consts import REGEX_MATCHED
from nonebot.log import logger
from nonebot.params import EventPlainText
from nonebot.rule import regex
from nonebot.typing import T_State

from .common import CONF, START
from .roll import roll

RE_ROLL_STR = (
    "^("  # 1
    + START
    + CONF.i7s_roll_command
    + " |"
    + CONF.i7s_roll_trigger
    #      2                     3  4      5                                    6
    + r" )([0-9adgimnsuvx+\- ]+)( ?(结果)?(大于|小于|大于等于|小于等于|>=|>|<|<=) ?(-?\d{1,10}))?"
)

RE_ROLL_CMD = re.compile(RE_ROLL_STR)

async def roll_command_handler(event: Event, msg: Annotated[str, EventPlainText()], state: T_State):
    messages = onebot11.Message() 

    logger.info(f"[7sRoll] received roll command: {msg}")

    if isinstance(event, onebot11.GroupMessageEvent):
        messages.append(onebot11.MessageSegment.at(event.user_id))
        messages.append('\n')

    match = None
    if REGEX_MATCHED in state:
        match = state[REGEX_MATCHED]
    else:
        args = msg.strip()
        match = RE_ROLL_CMD.match(args)
        if not match:
            messages.append("roll 命令格式错误\n")
            messages.append("格式为：roll <表达式>[ <判断方式><目标>]\n")
            messages.append("表达式举例：3d6+1d3-1\n")
            messages.append("判断方式可选：>, <, <=, >=, 或对应中文\n")
            messages.append("目标：需要达成的点数")
        elif match.group(1) is None:
            return

    if match:
        expr_str, op_str, target = match.group(2, 5, 6)
        messages.append('\n'.join(roll(expr_str, op_str, target)))

    return await cmd_roll.finish(messages)


cmd_roll = on_command(CONF.i7s_roll_command, priority=1, block=True)
cmd_roll.handle()(roll_command_handler)

message_cmd_roll = on_message(rule=regex(RE_ROLL_STR), priority=2, block=True)
message_cmd_roll.handle()(roll_command_handler)
