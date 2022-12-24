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
TODO
"""

PART_1_ANSWER = 0
PART_2_ANSWER = 0


def parse_input(input: str) -> str:
    return input.strip()

@timeit
def part1(input: str) -> int:
    return 0

@timeit
def part2(input: str) -> int:
    return 0

stdin = sys.stdin.read()
input = parse_input(stdin)
test_input = parse_input(TEST_INPUT)
info("=" * 40)
info(f"test 1: {part1(test_input)}")
# info(f"part 1: {part1(input)}")
# input = parse_input(stdin)
# test_input = parse_input(TEST_INPUT)
# info(f"test 2: {part2(test_input)}")
# info(f"part 2: {part2(input)}")