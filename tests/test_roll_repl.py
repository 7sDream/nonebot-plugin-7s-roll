import re


def test_roll_repl():
    from nonebot_plugin_7s_roll import roll

    regex = re.compile(r"^([0-9adgimnsuvx+\- ]+)( ?(>=|>|<|<=) ?(-?\d{1,10}))?$")
    while True:
        print()
        s = input("roll> ").strip()
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
