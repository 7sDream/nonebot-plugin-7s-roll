import re


def test_roll_repl():
    import nonebot
    from nonebot.adapters.cqhttp import Bot as CQHTTPBot

    nonebot.init()
    driver = nonebot.get_driver()
    driver.register_adapter("cqhttp", CQHTTPBot)
    nonebot.load_builtin_plugins()
    nonebot.load_plugin("nonebot_plugin_7s_roll")

    roll = nonebot.require("nonebot_plugin_7s_roll").roll

    regex = re.compile(r"^([0-9adgimnsuvx+\- ]+)( ?(>=|>|<|<=) ?(-?\d{1,10}))?$")
    while True:
        s = input("> ").strip()
        if s in {"q", "quit", "exit"}:
            break
        match = regex.match(s)
        if match:
            expr_str, op_str, target = match.group(1, 3, 4)
            messages = roll(expr_str, op_str, target)
            print("\n".join(messages))
            print()
        else:
            print("invalid input")
