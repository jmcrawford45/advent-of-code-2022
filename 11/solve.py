import os
import sys
from logging import *
basicConfig(level=INFO)
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from utils import *
from collections import *

TEST_INPUT = """
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""

PART_1_ANSWER = 0
PART_2_ANSWER = 0

class Monkey:
    def __init__(self):
        pass
    def __repr__(self):
        return f"Monkey({self.items=})"


def parse_input(input: str) -> list[Monkey]:
    monkeys = []
    monkey = None
    condition = true_branch = false_branch = None
    for line in input.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("Monkey"):
            if monkey:
                monkey.test = lambda x, true_branch=true_branch, false_branch=false_branch, condition=condition: (true_branch if x % condition == 0 else false_branch)
                monkeys.append(monkey)
            monkey = Monkey()
            condition = true_branch = false_branch = None
        elif line.startswith("Starting"):
            items = [int(c) for c in line.split(':')[1].strip().split(", ")]
            monkey.items = items
        elif line.startswith("Operation"):
            if line.endswith("* old"):
                monkey.op = lambda x: (x ** 2)
            elif '+' in line:
                c = int(line.split()[-1])
                monkey.op = lambda x, c=c: (x + c)
            elif '*' in line:
                c = int(line.split()[-1])
                monkey.op = lambda x, c=c: (x * c)
            else:
                raise ValueError()
        elif line.startswith("Test"):
            condition = int(line.split()[-1])
            monkey.condition = condition
        elif line.startswith("If true"):
            true_branch = int(line.split()[-1])
        elif line.startswith("If false"):
            false_branch = int(line.split()[-1])
        else:
            raise ValueError("failed to parse")
    if monkey:
        monkey.test = lambda x: (true_branch if x % condition == 0 else false_branch)
        monkeys.append(monkey)
    return monkeys


def part1(monkeys: list[Monkey]) -> int:
    inspects = defaultdict(int)
    for _ in range(20):
        for i, monkey in enumerate(monkeys):
            debug(f"monkey {i} has {len(monkey.items)} items")
            for item in monkey.items:
                item = monkey.op(item) // 3
                debug(f"worry after inspect: {item}")
                inspects[i] += 1
                throw_to = monkey.test(item)
                debug(f"{i} throws to {throw_to}")
                monkeys[throw_to].items.append(item)
            monkey.items = []
        debug(monkeys)
    top_2 = sorted(inspects.values(), reverse=True)[:2]

    return top_2[0] * top_2[1]

def part2(monkeys: list[Monkey]) -> int:
    inspects = defaultdict(int)
    gcd = 1
    for monkey in monkeys:
        gcd *= monkey.condition
    for _ in range(10000):
        for i, monkey in enumerate(monkeys):
            debug(f"monkey {i} has {len(monkey.items)} items")
            for item in monkey.items:
                item = monkey.op(item) % gcd
                debug(f"worry after inspect: {item}")
                inspects[i] += 1
                throw_to = monkey.test(item)
                debug(f"{i} throws to {throw_to}")
                monkeys[throw_to].items.append(item)
            monkey.items = []
        debug(monkeys)
    top_2 = sorted(inspects.values(), reverse=True)[:2]

    return top_2[0] * top_2[1]


input = parse_input(sys.stdin.read())
test_input = parse_input(TEST_INPUT)
info("=" * 40)
info(f"test 1: {part1(test_input)}")
info(f"part 1: {part1(input)}")
info(f"test 2: {part2(test_input)}")
info(f"part 2: {part2(input)}")