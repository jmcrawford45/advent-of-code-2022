import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from utils import *
from collections import *

TEST_INPUT = """
TODO
"""

PART_1_ANSWER = 0
PART_2_ANSWER = 0


def parse_input(input: str) -> str:
    return input.strip()


def part1(input: str) -> int:
    result = 0
    return result

def part2(input: str) -> int:
    result = 0
    return result


input = parse_input(sys.stdin.read())
test_input = parse_input(TEST_INPUT)
print("=" * 40)
print("test 1:", part1(test_input))
print("part 1:", part1(input))
print("test 2:", part2(test_input))
print("part 2:", part2(input))