import os
import sys

TEST_INPUT = """
forward 5
down 5
forward 8
up 3
down 8
forward 2"""

PART_1_ANSWER = 150
PART_2_ANSWER = 900


def parse_input(input: str) -> str:
    return input.strip()


def part1(input: str) -> int:
    x = y = 0
    for line in input.splitlines():
        dir, val = line.strip().split()
        val = int(val)
        if dir == "forward":
            x += val
        elif dir == "backward":
            x += -1 * val
        elif dir == "up":
            y += -1 * val
        elif dir == "down":
            y += val

    return x * y

def part2(input: str) -> int:
    x = aim = y = 0
    for line in input.splitlines():
        dir, val = line.strip().split()
        val = int(val)
        if dir == "forward":
            x += val
            y += aim * val
        elif dir == "backward":
            x += -1 * val
        elif dir == "up":
            aim += -1 * val
        elif dir == "down":
            aim += val

    return x * y


input = parse_input(sys.stdin.read())
test_input = parse_input(TEST_INPUT)
print("=" * 40)
print("test 1:", part1(test_input))
print("part 1:", part1(input))
print("test 2:", part2(test_input))
print("part 2:", part2(input))