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
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""

PART_1_ANSWER = 0
PART_2_ANSWER = 0


def parse_input(input: str) -> str:
    cubes = []
    for line in input.strip().splitlines():
        line = line.strip()
        cubes.append(tuple(int(a) for a in line.split(',')))
    return cubes
from copy import deepcopy
@timeit
def part1(input: list[list[int]]) -> int:
    exposed = 6 * len(input)
    for j, cube1 in enumerate(input):
        for i, cube2 in enumerate(input[j:]):
            if cube1 == cube2:
                continue
            for offset in [-1, 1]:
                for index in range(3):
                    cube3 = list(deepcopy(cube1))
                    cube3[index] += offset
                    if tuple(cube3) == cube2:
                        exposed -= 2
    return exposed

@timeit
def part2(input: list[tuple[int, int, int]]) -> int:
    input = set(input)
    max_edge = (0,0,0)
    internal_exposed = 0
    for cube in input:
        max_edge = tuple(max(a,b) for a,b in zip(max_edge, cube))
    min_edge = deepcopy(max_edge)
    for cube in input:
        min_edge = tuple(min(a,b) for a,b in zip(min_edge, cube))
    internal_exposed = 0
    queue = deque()
    min_edge = tuple(a-1 for a in min_edge)
    max_edge = tuple(a+1 for a in max_edge)
    queue.append(max_edge)
    seen = set()
    while queue:
        next_cube = queue.pop()
        if next_cube not in seen:
            seen.add(next_cube)
            for index, offset in [(0, -1), (0, 1),(1, -1), (1, 1),(2, -1), (2, 1)]:
                cube4 = list(deepcopy(next_cube))
                cube4[index] += offset
                cube4 = tuple(cube4)
                if cube4 in input:
                    internal_exposed += 1
                elif all(low <= a <= high for low, a, high in zip(min_edge, cube4, max_edge)):
                    queue.append(cube4)
    return internal_exposed


input = parse_input(sys.stdin.read())
test_input = parse_input(TEST_INPUT)
info("=" * 40)
info(f"test 1: {part1(test_input)}")
info(f"part 1: {part1(input)}")
info(f"test 2: {part2(test_input)}")
info(f"part 2: {part2(input)}")