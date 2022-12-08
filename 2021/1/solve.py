import os
import sys

TEST_INPUT = """
199
200
208
210
200
207
240
269
260
263"""

PART_1_ANSWER = 0
PART_2_ANSWER = 0


def parse_input(input: str) -> str:
    return input.strip()


def part1(input: str) -> int:
    m = [int(c) for c in input.splitlines()]
    count = 0
    for i in range(len(m) - 1):
        if m[i+1] > m[i]:
            count += 1 
    return count

def part2(input: str) -> int:
    m = [int(c) for c in input.splitlines()]
    count = 0
    for i in range(2, len(m) - 2):
        if sum(m[i:i+3]) > sum(m[i-1:i+2]):
            count += 1
    return count + 1


input = parse_input(sys.stdin.read())
test_input = parse_input(TEST_INPUT)
print("=" * 40)
print("test 1:", part1(test_input))
print("part 1:", part1(input))
print("test 2:", part2(test_input))
print("part 2:", part2(input))