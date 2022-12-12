import os
import sys
from logging import *
basicConfig(level=INFO)
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from utils import *
from collections import *

TEST_INPUT = """
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""

PART_1_ANSWER = 31


def parse_input(input: str) -> str:
    return input.strip()

def neighbors(point: tuple[int, int], grid: list[list[int]], visited: tuple[int, int]) -> set[tuple[int, int]]:
    dirs = [(0,1), (0, -1), (-1, 0), (1, 0)]
    x, y = point
    candidates = set()
    for d in dirs:
        delta_x, delta_y = d
        new = (x + delta_x, y + delta_y)
        if new not in visited and 0 <= new[0] < len(grid) and 0 <= new[1] < len(grid[0]):
            if grid[new[0]][new[1]] - grid[x][y] <= 1:
                candidates.add(new)
    return candidates



def part1(input: str) -> int:
    grid = []
    start = end = None
    for row, line in enumerate(input.splitlines()):
        grid_row = []
        line = line.strip()
        debug(line)
        for col, char in enumerate(line):
            if char == "S":
                start = (row, col)
                char = "a"
            elif char == "E":
                end = (row, col)
                char = "z"
            grid_row.append(ord(char) - ord("a"))
        grid.append(grid_row)
    queue = deque()
    queue.append((start, 0))
    visited = set()
    while queue:
        next, depth = queue.popleft()
        if next == end:
            return depth
        depth += 1
        debug(len(visited))
        visited.add(next)
        for point in neighbors(next, grid, visited):
            if (point, depth) not in queue:
                queue.append((point, depth))    

def part2(input: str) -> int:
    grid = []
    starts = []
    end = None
    for row, line in enumerate(input.splitlines()):
        grid_row = []
        line = line.strip()
        debug(line)
        for col, char in enumerate(line):
            if char == "S":
                starts.append((row, col))
                char = "a"
            elif char == "E":
                end = (row, col)
                char = "z"
            if char == "a":
                starts.append((row, col))
            grid_row.append(ord(char) - ord("a"))
        grid.append(grid_row)
    queue = deque()
    for start in starts:
        queue.append((start, 0))
    visited = set()
    while queue:
        next, depth = queue.popleft()
        if next == end:
            return depth
        depth += 1
        debug(len(visited))
        visited.add(next)
        for point in neighbors(next, grid, visited):
            if (point, depth) not in queue:
                queue.append((point, depth))   


input = parse_input(sys.stdin.read())
test_input = parse_input(TEST_INPUT)
info("=" * 40)
info(f"test 1: {part1(test_input)}")
info(f"part 1: {part1(input)}")
info(f"test 2: {part2(test_input)}")
info(f"part 2: {part2(input)}")