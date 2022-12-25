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
        debug(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper


TEST_INPUT = """
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
"""

PART_1_ANSWER = 0
PART_2_ANSWER = 0

def from_snafe_char(input: str) -> int:
    if input == "=":
        return -2
    if input == "-":
        return -1
    return int(input)

def from_snafu(input: str) -> int:
    input = input.strip()
    return sum(from_snafe_char(char)* 5 ** i for i, char in enumerate(reversed(input)))

def to_snafu(input: int) -> str:
    out = ""
    carry = 0
    while input:
        next = (input) % 5
        carry = 0
        if next < 3:
            out += str(next)
        elif next == 4:
            out += "-"
            carry += 1
        else:
            out += "="
            carry += 1

        input = input // 5 + carry 
    return ''.join(reversed(out))


def parse_input(input: str) -> str:
    nums = []
    for line in input.strip().splitlines():
        nums.append(from_snafu(line))
    return nums

@timeit
def part1(input: list[int]) -> int:
    return to_snafu(sum(input))

@timeit
def part2(input: str) -> int:
    return 0

stdin = sys.stdin.read()
input = parse_input(stdin)
test_input = parse_input(TEST_INPUT)
info("=" * 40)
info(f"test 1: {part1(test_input)}")
info(f"part 1: {part1(input)}")
# input = parse_input(stdin)
# test_input = parse_input(TEST_INPUT)
# info(f"test 2: {part2(test_input)}")
# info(f"part 2: {part2(input)}")