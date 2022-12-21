import os
import sys
from logging import *
basicConfig(level=INFO)
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from utils import *
from collections import *
from functools import lru_cache
from dataclasses import dataclass

from functools import wraps
import time


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        # debug(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper


TEST_INPUT = """
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
"""

PART_1_ANSWER = 0
PART_2_ANSWER = 0

@dataclass
class Monkey:
    name: str
    val: int | None = None
    deps: tuple["Monkey"] = ()
    dependees: tuple["Monkey"] = ()
    op: str | None = None


def parse_input(input: str) -> str:
    graph = {}
    for line in input.strip().splitlines():
        line = line.strip()
        name, val = line.split(': ')[:2]
        graph[name] = Monkey(name)
    for line in input.strip().splitlines():
        line = line.strip()
        name, val = line.split(': ')[:2]
        try:
            graph[name].val = int(val)
        except:
            dep1, op, dep2 = val.split()[:3]
            graph[name].op = op
            graph[name].deps = (dep1, dep2)
            graph[dep1].dependees += (name,)
            graph[dep2].dependees += (name,)
    
    return graph

@timeit
def part1(input: dict[str, Monkey]) -> int:
    to_resolve = set(input)
    while "root" in to_resolve:
        for name in set(input) & to_resolve:
            monkey = input[name]
            if monkey.val is not None:
                to_resolve.remove(monkey.name)
            elif all(a not in to_resolve for a in monkey.deps):
                val1 = input[monkey.deps[0]].val
                val2 = input[monkey.deps[1]].val
                if monkey.op == "/":
                    monkey.val = val1 / val2
                elif monkey.op == "*":
                    monkey.val = val1 * val2
                elif monkey.op == "-":
                    monkey.val = val1 - val2
                elif monkey.op == "+":
                    monkey.val = val1 + val2
                to_resolve.remove(monkey.name)

    return input["root"].val

def invert_monkey(monkey: Monkey, input: dict[str, Monkey]) -> str:
    output = [input[a] for a in monkey.dependees if input[a].val is not None][0]
    val = output.val
    input1 = [input[a].val for a in output.deps if input[a].val is not None][0]
    to_fix = [input[a] for a in output.deps if input[a].val is None][0]
    need_first = to_fix == input[output.deps[0]]
    if output.op == "/" and need_first:
        monkey.val = val * input1
    elif output.op == "/":
        to_fix.val = input1 / val
    elif output.op == "*":
        to_fix.val = val / input1
    elif output.op == "-" and need_first:
        to_fix.val = input1 + val
    elif output.op == "-":
        to_fix.val = input1 - val
    elif output.op == "+":
        to_fix.val = val - input1
    debug(f"fixed {to_fix.name} with {to_fix.val=} because {monkey.name=} was {monkey.val=}")
    return to_fix.name

from time import sleep
@timeit
def part2(input: dict[str, Monkey]) -> int:
    to_resolve = set(input)
    input["humn"].val = None
    last_len_resolve = -1
    while len(to_resolve) != last_len_resolve:
        last_len_resolve = len(to_resolve)
        for name in set(input) & to_resolve:
            monkey = input[name]
            if monkey.val is not None:
                to_resolve.remove(monkey.name)
            elif monkey.deps and all(a not in to_resolve for a in monkey.deps):
                val1 = input[monkey.deps[0]].val
                val2 = input[monkey.deps[1]].val
                if monkey.op == "/":
                    monkey.val = val1 / val2
                elif monkey.op == "*":
                    monkey.val = val1 * val2
                elif monkey.op == "-":
                    monkey.val = val1 - val2
                elif monkey.op == "+":
                    monkey.val = val1 + val2
                to_resolve.remove(monkey.name)
    debug([a for a in input["root"].deps if input[a].val is None])
    target = [a for a in input["root"].deps if input[a].val is None][0]
    solved = [a for a in input["root"].deps if input[a].val is not None][0]
    input[target].val = input[solved].val
    to_resolve.remove(target)
    debug(f"{len(to_resolve)=}")
    while "humn" in to_resolve:
        for name in set(input) & to_resolve:
            monkey = input[name]
            for a in monkey.dependees:
                if input[a].val is not None and any(input[b].val is not None for b in input[a].deps):
                    invert_monkey(monkey, input)
                    to_resolve.remove(monkey.name)
    return input["humn"].val


raw_stdin = sys.stdin.read()
input = parse_input(raw_stdin)
test_input = parse_input(TEST_INPUT)
info("=" * 40)
info(f"test 1: {part1(test_input)}")
info(f"part 1: {part1(input)}")
input = parse_input(raw_stdin)
test_input = parse_input(TEST_INPUT)
info(f"test 2: {part2(test_input)}")
info(f"part 2: {part2(input)}")