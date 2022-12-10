import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from utils import *
from collections import *

TEST_INPUT = """
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""

PART_1_ANSWER = 0
PART_2_ANSWER = 0


def parse_input(input: str) -> str:
    return input.strip()


def part1(input: str) -> int:
    cycle = 1
    register = 1
    sum_vals = 0
    seen = set()
    for line in input.splitlines():
        line = line.strip()
        if cycle in [20, 60, 100, 140, 180, 220]:
            seen.add(cycle)
            sum_vals += register * cycle
        elif cycle in [21, 61, 101, 141, 181, 221] and cycle - 1 not in seen:
            sum_vals += (register - val) * (cycle-1)
            seen.add(cycle - 1)
        if line.startswith("noop"):
            cycle += 1
        else:
            val = int(line.split()[1])
            cycle += 2
            register += val



    return sum_vals

def part2(input: str) -> int:
    cycle = 0
    register = 1
    start = [["."] * 40 for _ in range(6)]
    for line in input.splitlines():
        line = line.strip()
        if line.startswith("noop"):
            if abs(cycle % 40 - register) <= 1:
                start[cycle // 40][cycle % 40] = "#"
            cycle += 1
        else:
            if abs(cycle % 40 - register) <= 1:
                start[cycle // 40][cycle % 40] = "#"
            cycle += 1
            if abs(cycle % 40 - register) <= 1:
                start[cycle // 40][cycle % 40] = "#"
            cycle += 1
            val = int(line.split()[1])
            register += val
    for row in start:
        print(''.join(row))


input = parse_input(sys.stdin.read())
test_input = parse_input(TEST_INPUT)
print("=" * 40)
print("test 1:", part1(test_input))
print("part 1:", part1(input))
print("test 2:", part2(test_input))
print("part 2:", part2(input))