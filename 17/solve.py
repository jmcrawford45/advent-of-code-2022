import os
import sys
from logging import *
basicConfig(level=INFO)
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from utils import *
from collections import *

from functools import wraps
import time
from copy import deepcopy


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        info(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper


TEST_INPUT = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""

PART_1_ANSWER = 0
PART_2_ANSWER = 0


def parse_input(input: str) -> str:
    return input.strip()

def place_rock(cave: list[list[str]], rock: list[list[str]], offset: tuple[int, int]):
    x_offset, y_offset = offset
    for i in range(len(rock)):
        for j in range(len(rock[0])):
            if rock[i][j] == '#':
                cave[y_offset + i][x_offset + j] = '#' 

def can_place(cave: list[list[str]], rock: list[list[str]], offset: tuple[int, int]) -> bool:
    x_offset, y_offset = offset
    for i in range(len(rock)):
        for j in range(len(rock[0])):
            if rock[i][j] == '#' and not (0 <= x_offset + j < len(cave[0])):
                return False
            if rock[i][j] == '#' and  not (0 <= y_offset + i < len(cave)):
                return False
            if rock[i][j] == '#' and cave[y_offset + i][x_offset + j] == '#':
                return False
    return True

def solve2(rounds: int, input: str) -> int:
    cave = [["."] * 7 for _ in range(100000)]
    rocks = [
        [
            list('####'),
        ],
        [
            list('.#.'),
            list('###'),
            list('.#.'),
        ],
        [
            list('###'),
            list('..#'),
            list('..#'),
        ],
        [
            list('#'),
            list('#'),
            list('#'),
            list('#'),
        ],
        [
            list('##'),
            list('##'),
        ]
    ]
    rock_num = 0
    move_num = 0
    max_height = 0
    x_offset = 2
    y_offset = 3
    cycle_gain = 0
    dp = {(0,0) + (0,) * len(cave[0]): (0, 0)}
    while rock_num < rounds:
        rock = rocks[rock_num % len(rocks)]
        if rock_num == 1:
            cave_copy = deepcopy(cave)
            place_rock(cave_copy, rock, (x_offset, y_offset))
            for i in reversed(range(y_offset + 1)):
                debug('|' + ''.join(cave_copy[i]) + '|')
            debug("+-------+")
        if input[move_num % len(input)] == '<':
            if can_place(cave, rock, (x_offset - 1, y_offset)):
                debug("move left")
                x_offset -= 1
            else:
                debug("hit left wall")
        elif can_place(cave, rock, (x_offset + 1, y_offset)):
            debug("move right")
            x_offset += 1
        else:
            debug("hit right wall")
        move_num += 1
        if not can_place(cave, rock, (x_offset, y_offset - 1)):
            place_rock(cave, rock, (x_offset, y_offset))
            x_offset = 2
            max_height = max(max_height, y_offset + len(rock))
            y_offset = max_height + 3
            rock_num += 1
            max_heights = [-1 * max_height] * len(cave[0])
            max_height_check = max_height
            while max_height_check > 0:
                for x in range(len(cave[0])):
                    if cave[max_height_check - 1][x] == '#' and max_heights[x] == -1 * max_height:
                        max_heights[x] = max_height_check - max_height
                max_height_check -= 1
            key = (rock_num % len(rocks), move_num % len(input)) + tuple(max_heights)
            if key in dp:
                info(f"cycle detected at round {rock_num} {key=}")
                prev_rock_num, prev_max_height = dp[key]
                height_gain = max_height - prev_max_height
                rock_gain = rock_num - prev_rock_num
                num_cycles= (rounds - rock_num) // rock_gain
                remaining_rocks = (rounds - rock_num) % rock_gain
                cycle_gain = num_cycles * height_gain
                info(f"{num_cycles=} {remaining_rocks=} {rock_gain=}")
                dp.clear()
                rock_num = rounds - remaining_rocks
            dp[key] = (rock_num, max_height)
            for i in reversed(range(y_offset)):
                debug('|' + ''.join(cave[i]) + '|')
            debug("+-------+")
        else:
            y_offset -= 1
    return max_height + cycle_gain

@timeit
def part1(input: str) -> int:
    return solve2(2022, input)

@timeit
def part2(input: str) -> int:
    return solve2(1000000000000, input)


input = parse_input(sys.stdin.read())
test_input = parse_input(TEST_INPUT)
info("=" * 40)
info(f"test 1: {part1(test_input)}")
info(f"part 1: {part1(input)}")
info(f"test 2: {part2(test_input)}")
info(f"part 2: {part2(input)}")