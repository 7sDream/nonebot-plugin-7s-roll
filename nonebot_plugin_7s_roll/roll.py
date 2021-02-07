import re
import operator

from .expr import compile, Roll

OP_MAP = {
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
    "大于": operator.gt,
    "大于等于": operator.ge,
    "小于": operator.lt,
    "小于等于": operator.le,
}


def roll(expr_str: str, op_str: str = None, target_str: str = None) -> [str]:
    messages = []

    try:
        expr = compile(expr_str)
    except:
        expr = None

    if expr is None:
        messages.append("roll 命令表达式错误")
        messages.append("表达式举例：3d6+1d3-1")
        return messages

    op = None
    if op_str:
        op = OP_MAP[op_str]
        target = int(target_str)

    message = [f"{expr_str.strip()} 投掷结果"]
    if op:
        message.append(f"(目标 {op_str} {target})：")
    messages.append("".join(message))

    result, display = expr()

    if isinstance(expr, Roll):  # 单纯扔一个骰子
        roll: Roll = expr
        dices = roll.values

        messages.append("")

        for i, dice in enumerate(dices):
            message = [f"第 {i+1} 颗：{dice}"]
            if op:
                if op(dice, target):
                    message.append("，通过")
                else:
                    message.append("，未通过")
            messages.append("".join(message))

        if len(dices) > 1:
            prefix = roll.post_processor.prefix
            messages.append("")
            message = [f"{prefix} {result}"]
            if op:
                if op(result, target):
                    message.append("，通过")
                else:
                    message.append("，未通过")
            messages.append("".join(message))
    else:
        message = [display, " = ", str(result)]
        if op:
            if op(result, target):
                message.append("，通过")
            else:
                message.append("，未通过")
        messages.append("".join(message))

    return messages
