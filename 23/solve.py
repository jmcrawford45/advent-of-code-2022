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
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#.."""

from copy import deepcopy


def parse_input(input: str) -> tuple[int, int]:
    elves = set()
    for row, line in enumerate(input.strip().splitlines()):
        for col, char in enumerate(line):
            if char == "#":
                elves.add((row, col))

    return elves

def get_neighbors(elf: tuple[int, int]) -> Iterable[tuple[int, int]]:
    out = []
    row, col = elf
    for col_offset in range(-1, 2):
        for row_offset in range(-1, 2):
            if not (row_offset == 0 and col_offset == 0):
                out.append((row + row_offset, col + col_offset))
    return out

def move_candidates(neighbors: Iterable[tuple[int, int]], offset: int, elf: tuple[int, int]) -> Iterable[tuple[int, int]]:
    if offset % 4 == 0:
        return [n for n in neighbors if n[0] - elf[0] == -1]
    elif offset % 4 == 1:
        return [n for n in neighbors if n[0] - elf[0] == 1]
    if offset % 4 == 2:
        return [n for n in neighbors if n[1] - elf[1] == -1]
    elif offset % 4 == 3:
        return [n for n in neighbors if n[1] - elf[1] == 1]




@timeit
def part1(input: tuple[int, int]) -> int:
    elves = deepcopy(input)
    for round in range(10):
        proposed_moves = defaultdict(list)
        for elf in elves:
            neighbors = list(get_neighbors(elf))
            if not set(neighbors) & elves:
                continue
            for i in range(4):
                candidates = move_candidates(neighbors, round + i, elf)
                if not (set(candidates) & elves):
                    for n in candidates:
                        if abs(n[0] - elf[0]) + abs(n[1] - elf[1]) == 1:
                            proposed_moves[n].append(elf)
                    break
        for end, start in proposed_moves.items():
            if len(start) == 1:
                elves.remove(start[0])
                elves.add(end)


    return abs(max(e[0] for e in elves) - min(e[0] for e in elves) + 1) * abs(max(e[1] for e in elves) - min(e[1] for e in elves) + 1) - len(elves)

def draw(elves):
    out = "\n"
    max_row = max(e[0] for e in elves)
    min_row = min(e[0] for e in elves)
    max_col = max(e[1] for e in elves)
    min_col = min(e[1] for e in elves)
    for row in range(min_row, max_row + 1):
        for col in range(min_col, max_col + 1):
            out += "#" if (row, col) in elves else "."
        out += "\n"
    debug(out)

@timeit
def part2(input: str) -> int:
    elves = deepcopy(input)
    round = 0
    debug("Initial state")
    draw(elves)
    while True:
        moved = False
        proposed_moves = defaultdict(list)
        for elf in elves:
            neighbors = list(get_neighbors(elf))
            if not set(neighbors) & elves:
                continue
            for i in range(4):
                candidates = move_candidates(neighbors, round + i, elf)
                if not (set(candidates) & elves):
                    for n in candidates:
                        if abs(n[0] - elf[0]) + abs(n[1] - elf[1]) == 1:
                            proposed_moves[n].append(elf)
                    break
        for end, start in proposed_moves.items():
            if len(start) == 1:
                elves.remove(start[0])
                elves.add(end)
                moved = True
        for k, v in proposed_moves.items():
            debug(f"{k}: {v}")
        draw(elves)
        debug(f"End of round {round + 1}")
        if not moved:
            return round + 1
        round += 1

stdin = sys.stdin.read()
input = parse_input(stdin)
test_input = parse_input(TEST_INPUT)
info("=" * 40)
info(f"test 1: {part1(test_input)}")
info(f"part 1: {part1(input)}")
input = parse_input(stdin)
test_input = parse_input(TEST_INPUT)
info(f"test 2: {part2(test_input)}")
info(f"part 2: {part2(input)}")