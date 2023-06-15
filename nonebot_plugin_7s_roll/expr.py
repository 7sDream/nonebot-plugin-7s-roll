import abc
import math
import random
import re
from typing import Dict, List, Optional, Tuple


class Op(abc.ABC):
    @abc.abstractmethod
    def __call__(self, left: Tuple[int, str], right: Tuple[int, str]) -> Tuple[int, str]:
        pass


class __Add(Op):
    def __call__(self, left: Tuple[int, str], right: Tuple[int, str]) -> Tuple[int, str]:
        val = left[0] + right[0]
        return val, f"{left[1]} + {right[1]}"


class __Minus(Op):
    def __call__(self, left: Tuple[int, str], right: Tuple[int, str]) -> Tuple[int, str]:
        val = left[0] - right[0]
        return val, f"{left[1]} - {right[1]}"


ADD = __Add()
MINUS = __Minus()

OP_MAP = {
    "+": ADD,
    "-": MINUS,
}


class PostProcessor(abc.ABC):
    @abc.abstractproperty
    def prefix(self):
        pass

    @abc.abstractmethod
    def __call__(self, values: List[int]) -> Tuple[int, str]:
        pass


class __MaxPostProcessor(PostProcessor):
    @property
    def prefix(self):
        return "最大值为"

    def __call__(self, values: List[int]) -> Tuple[int, str]:
        val = max(values)
        if len(values) == 1:
            s = str(val)
        else:
            s = "".join(["(max[", ", ".join(map(str, values)), "] = ", str(val), ")"])
        return val, s


class __MinPostProcessor(PostProcessor):
    @property
    def prefix(self):
        return "最小值为"

    def __call__(self, values: List[int]) -> Tuple[int, str]:
        val = min(values)
        if len(values) == 1:
            s = str(val)
        else:
            s = "".join(["(min[", ", ".join(map(str, values)), "] = ", str(val), ")"])
        return val, s


class __AvgPostProcessor(PostProcessor):
    @property
    def prefix(self):
        return "平均值为"

    def __call__(self, values: List[int]) -> Tuple[int, str]:
        val = math.floor(sum(values) / len(values))
        if len(values) == 1:
            s = str(val)
        else:
            s = "".join(["(avg[", ", ".join(map(str, values)), "] = ", str(val), ")"])
        return val, s


class __SumPostProcessor(PostProcessor):
    @property
    def prefix(self):
        return "总和为"

    def __call__(self, values: List[int]) -> Tuple[int, str]:
        val = sum(values)
        if len(values) == 1:
            s = str(val)
        else:
            s = "".join(["(", " + ".join(map(str, values)), ")"])
        return val, s


MAX = __MaxPostProcessor()
MIN = __MinPostProcessor()
AVG = __AvgPostProcessor()
SUM = __SumPostProcessor()

POST_PROCESS_MAP: Dict[str, PostProcessor] = {
    "max": MAX,
    "min": MIN,
    "avg": AVG,
    "sum": SUM,
}


class Expr(abc.ABC):
    @abc.abstractmethod
    def __call__(self) -> Tuple[int, str]:
        pass


class OpExpr(Expr):
    def __init__(self, left: Expr, op: Op, right: Expr):
        self.left = left
        self.op = op
        self.right = right

    def __call__(self) -> Tuple[int, str]:
        return self.op(self.left(), self.right())


class Num(Expr):
    def __init__(self, val):
        self.val = val

    def __call__(self):
        return self.val, str(self.val)


class Roll(Expr):
    post_processor: PostProcessor

    def __init__(self, times: int, faces: int, postprocessor: Optional[PostProcessor] = None):
        self.times = times
        self.faces = faces
        self.post_processor = SUM
        if postprocessor is not None:
            self.post_processor = postprocessor
        self.values = []

    def __call__(self):
        self.values = [random.randint(1, self.faces) for _ in range(self.times)]
        return self.post_processor(self.values)


RE_ROLL = re.compile(r"(\d+){1,2}[dD](\d+){1,4}(min|max|avg|sum|取小|取大|平均|求和)?")
RE_OP = re.compile(r"[+\-]")
RE_NUM = re.compile(r"\d+")


def tokenize(s: str) -> Optional[List[Expr]]:
    s = s.replace(" ", "")
    tokens = []
    pos = 0
    roll_count = 0
    while pos < len(s):
        match = RE_ROLL.match(s, pos)
        if match:
            pos = match.end()
            times, faces, post = match.group(1, 2, 3)
            times = int(times)
            faces = int(faces)
            if times == 0 or times > 20:
                return None
            if faces == 0 or faces > 1000:
                return None
            if isinstance(post, str):
                post = POST_PROCESS_MAP[post]
            tokens.append(Roll(times, faces, post))
            roll_count += 1
            if roll_count > 20:
                return None
            continue
        match = RE_OP.match(s, pos)
        if match:
            pos = match.end()
            tokens.append(OP_MAP[match.group(0)])
            continue
        match = RE_NUM.match(s, pos)
        if match:
            pos = match.end()
            tokens.append(Num(int(match.group(0))))
            continue
        return None
    return tokens


def parse(tokens: Optional[List[Expr]]) -> Optional[Expr]:
    if tokens is None:
        return None
    while True:
        i = 0
        expr = None
        for i, item in enumerate(tokens):
            if isinstance(item, Op):
                if i == 0 or i == len(tokens) - 1:
                    return None
                pre = tokens[i - 1]
                nxt = tokens[i + 1]
                if not isinstance(pre, Expr) or not isinstance(nxt, Expr):
                    return None
                expr = OpExpr(pre, item, nxt)
                break
        if expr is not None:
            tokens[i - 1 : i + 2] = [expr]
        else:
            break
    if len(tokens) != 1:
        return None
    ast = tokens[0]

    if not isinstance(ast, Expr) or isinstance(ast, Num):
        return None

    return ast


def compile(s) -> Optional[Expr]:
    return parse(tokenize(s))
