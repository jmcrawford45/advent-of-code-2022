import os
import sys

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
    def __init__(self, items: list[int] = None, op: Callable[int, int] = None, test: Callable[int, int] = None):
        self.test = test
        self.op = op
        self.items = items
    def __repr__(self):
        return f"Monkey({self.items=})"


def parse_input(input: str) -> str:
    return input.strip()


def part1(input: str) -> int:
    monkeys = []
    monkey = None
    condition = None
    true_branch = None
    inspects = defaultdict(int)
    for line in input.splitlines():
        if not line:
            continue
        line = line.strip()
        if line.startswith("Monkey"):
            if monkey:
                monkeys.append(monkey)
            monkey = Monkey()
            condition = true_branch = false_branch = None
        elif line.startswith("Starting"):
            items = [int(c) for c in line.split(':')[1].strip().split(", ")]
            monkey.items = items
        elif line.startswith("Operation"):
            monkey.op = line
        elif line.startswith("Test"):
            monkey.condition = int(line.split()[-1])
        elif line.startswith("If true"):
            monkey.true_branch = int(line.split()[-1])
        elif line.startswith("If false"):
            monkey.false_branch = int(line.split()[-1])
        else:
            print(line)
            raise ValueError()
    if monkey:
        monkey.test = lambda x: true_branch if x % condition == 0 else false_branch
        monkeys.append(monkey)
    for _ in range(20):
        for i, monkey in enumerate(monkeys):
            print(f"monkey {i} has {len(monkey.items)} items")
            for j, item in enumerate(monkey.items):
                line = monkey.op
                op = lambda x: x
                if line.endswith("* old"):
                    op = lambda x: x ** 2
                elif '+' in line:
                    op = lambda x: x + int(line.split()[-1])
                elif '*' in line:
                    op = lambda x: x * int(line.split()[-1])
                
                item = op(item) // 3
                print(f"worry after inspect: {item}")
                inspects[i] += 1
                throw_to = monkey.true_branch if item % monkey.condition == 0 else monkey.false_branch
                print(f"{i} throws to {throw_to}")
                if i == throw_to:
                    return 0
                monkeys[throw_to].items.append(item)
            monkey.items = []
        print(monkeys)
    top_2 = sorted(inspects.values(), reverse=True)[:2]

    return top_2[0] * top_2[1]

def part2(input: str) -> int:
    monkeys = []
    monkey = None
    condition = None
    true_branch = None
    inspects = defaultdict(int)
    for line in input.splitlines():
        if not line:
            continue
        line = line.strip()
        if line.startswith("Monkey"):
            if monkey:
                monkeys.append(monkey)
            monkey = Monkey()
            condition = true_branch = false_branch = None
        elif line.startswith("Starting"):
            items = [int(c) for c in line.split(':')[1].strip().split(", ")]
            monkey.items = items
        elif line.startswith("Operation"):
            monkey.op = line
        elif line.startswith("Test"):
            monkey.condition = int(line.split()[-1])
        elif line.startswith("If true"):
            monkey.true_branch = int(line.split()[-1])
        elif line.startswith("If false"):
            monkey.false_branch = int(line.split()[-1])
        else:
            print(line)
            raise ValueError()
    if monkey:
        monkey.test = lambda x: true_branch if x % condition == 0 else false_branch
        monkeys.append(monkey)
    gcd = 1
    for monkey in monkeys:
        gcd *= monkey.condition
    for _ in range(10000):
        for i, monkey in enumerate(monkeys):
            # print(f"monkey {i} has {len(monkey.items)} items")
            for j, item in enumerate(monkey.items):
                line = monkey.op
                op = lambda x: x
                if line.endswith("* old"):
                    op = lambda x: x ** 2
                elif '+' in line:
                    op = lambda x: x + int(line.split()[-1])
                elif '*' in line:
                    op = lambda x: x * int(line.split()[-1])
                
                item = op(item) % gcd
                # print(f"worry after inspect: {item}")
                inspects[i] += 1
                throw_to = monkey.true_branch if item % monkey.condition == 0 else monkey.false_branch
                # print(f"{i} throws to {throw_to}")
                if i == throw_to:
                    return 0
                monkeys[throw_to].items.append(item)
            monkey.items = []
        # print(monkeys)
    top_2 = sorted(inspects.values(), reverse=True)[:2]

    return top_2[0] * top_2[1]


input = parse_input(sys.stdin.read())
test_input = parse_input(TEST_INPUT)
print("=" * 40)
print("test 1:", part1(test_input))
print("part 1:", part1(input))
print("test 2:", part2(test_input))
print("part 2:", part2(input))