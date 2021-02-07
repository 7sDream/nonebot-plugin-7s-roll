import re

from nonebot import on_message, on_command
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp.permission import GROUP
from nonebot.rule import regex

from .common import START, SEP, CONF
from .roll import roll

RE_ROLL_STR = (
    "^("  # 1
    + START
    + CONF.i7s_roll_command
    + " |"
    + CONF.i7s_roll_trigger
    #      2                     3  4      5                                    6
    + r" )?([0-9adgimnsuvx+\- ]+)( ?(结果)?(大于|小于|大于等于|小于等于|>=|>|<|<=) ?(-?\d{1,10}))?"
)

RE_ROLL_CMD = re.compile(RE_ROLL_STR)


async def roll_command_handler(bot: Bot, event: Event, state: dict):
    messages = []

    if await GROUP(bot, event):
        messages.append(f"[CQ:at,qq={event.user_id}]")

    match = None
    if "_match" in state:
        match = state["_matched"]
    else:
        args = str(event.message).strip()
        match = RE_ROLL_CMD.match(args)
        if not match:
            messages.append("roll 命令格式错误")
            messages.append("格式为：roll <表达式>[ <判断方式><目标>]")
            messages.append("表达式举例：3d6+1d3-1")
            messages.append("判断方式可选：>, <, <=, >=, 或对应中文")
            messages.append("目标：需要达成的点数")
            return await cmd_roll.finish("\n".join(messages))
        if match.group(1) is None:
            return

    expr_str, op_str, target = match.group(2, 5, 6)

    messages.extend(roll(expr_str, op_str, target))

    return await cmd_roll.finish("\n".join(messages))


cmd_roll = on_command(CONF.i7s_roll_command, priority=1, block=True)
cmd_roll.handle()(roll_command_handler)

message_cmd_roll = on_message(rule=regex(RE_ROLL_STR), priority=2, block=True)
message_cmd_roll.handle()(roll_command_handler)
