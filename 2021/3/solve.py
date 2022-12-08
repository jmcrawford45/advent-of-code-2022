import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from utils import *
from collections import *

TEST_INPUT = """
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""

PART_1_ANSWER = 198
PART_2_ANSWER = 0


def parse_input(input: str) -> str:
    return input.strip()


def part1(input: str) -> int:
    gamma = epsilon = ""
    transposed = transpose_lines(input.splitlines())
    for line in transposed:
        common = Counter(line).most_common()[0][0]
        gamma += common
        epsilon += "1" if common == "0" else "0"
    return int(gamma, 2) * int(epsilon, 2)

def part2(input: str) -> int:
    lines = []
    for line in input.splitlines():
        line = [c for c in line.strip()]
        lines.append(line)
    gamma = epsilon = ""
    indexes = list(range(len(lines)))
    for col in range(len(lines[0])):
        to_keep = []
        for row in range(len(lines)):
            if row in indexes and lines[row][col] == "1":
                to_keep.append(row)
        if len(to_keep) >= len(indexes) - len(to_keep):
            indexes = [i for i in indexes if i in to_keep]
        else:
            indexes = [i for i in indexes if i not in to_keep]
    gamma = int(''.join(lines[indexes[0]]), 2)
    indexes = list(range(len(lines)))
    for col in range(len(lines[0])):
        if len(indexes) == 1:
            break
        to_keep = []
        for row in range(len(lines)):
            if row in indexes and lines[row][col] == "1":
                to_keep.append(row)
        if len(to_keep) >= len(indexes) - len(to_keep):
            indexes = [i for i in indexes if i not in to_keep]
        else:
            indexes = [i for i in indexes if i in to_keep]
    epsilon = int(''.join(lines[indexes[0]]), 2)
    return gamma * epsilon


input = parse_input(sys.stdin.read())
test_input = parse_input(TEST_INPUT)
print("=" * 40)
print("test 1:", part1(test_input))
print("part 1:", part1(input))
print("test 2:", part2(test_input))
print("part 2:", part2(input))