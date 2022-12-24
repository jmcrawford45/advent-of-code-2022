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
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""

PART_1_ANSWER = 0
PART_2_ANSWER = 0



@dataclass
class Blizzard:
    symbol: str
    position: dict[int, tuple[int, int]]

@dataclass
class Map:
    board: list[list[str]]
    blizzards: list[Blizzard]
    curr: tuple[int, int]
    goal: tuple[int, int]
    can_move_cache: dict[tuple[tuple[int, int], int], bool]
    neighbors_cache: dict[tuple[tuple[int, int], int], tuple[tuple[int, int]]]
    blizzard_positions_cache: dict[int, tuple[int, int]]
    max_turn: int = 0

    def swap_goals(self):
        return Map(self.board, self.blizzards, self.goal, self.curr, {}, {}, {})
        
    def blizzard_positions(self, turn: int) -> set[tuple[int, int]]:
        if turn not in self.blizzard_positions_cache:
            self.move_blizzards(turn)
            self.blizzard_positions_cache[turn] = set(b.position[turn] for b in self.blizzards)
        return self.blizzard_positions_cache[turn]

    
    def in_bounds(self, pos: tuple[int, int]) -> bool:
        i,j = pos
        return 0 <= i < len(self.board) and 0 <= j < len(self.board[0])

    def move_blizzards(self, turn: int):
        if turn < self.max_turn:
            return
        for t in range(self.max_turn, turn + 1):
            for blizzard in self.blizzards:
                i, j = blizzard.position[t]
                if blizzard.symbol == "<":
                    if self.in_bounds((i, j-1)) and self.board[i][j-1] != "#":
                        next_pos = (i, j-1)
                    else:
                        next_pos = (i, len(self.board[i]) - 1 - list(reversed(self.board[i])).index("."))
                elif blizzard.symbol == ">":
                    if self.in_bounds((i, j+1)) and self.board[i][j+1] != "#":
                        next_pos = (i, j+1)
                    else:
                        next_pos = (i, self.board[i].index("."))
                elif blizzard.symbol == "v":
                    if self.in_bounds((i+1, j)) and self.board[i+1][j] != "#":
                        next_pos = (i+1, j)
                    else:
                        next_pos = ([self.board[c][j] for c in range(len(self.board))].index("."), j)
                elif blizzard.symbol == "^":
                    if self.in_bounds((i-1, j)) and self.board[i-1][j] != "#":
                        next_pos = (i-1, j)
                    else:
                        next_pos = (len(self.board) - 1 - [self.board[c][j] for c in reversed(range(len(self.board)))].index("."), j)
                blizzard.position[t + 1] = next_pos
        self.max_turn = max(self.max_turn, turn + 1)

    def can_move(self, position: tuple[int, int], turn: int) -> bool:
        if (position, turn) not in self.can_move_cache:
            row, col = position
            res = self.in_bounds(position) and not position in self.blizzard_positions(turn) and self.board[row][col] == "."
            self.can_move_cache[(position, turn)] = res
        return self.can_move_cache[(position, turn)]
    
    def neighbors(self, position: tuple[int, int], turn: int) -> tuple[tuple[int, int]]:
        if (position, turn) not in self.neighbors_cache:
            self.move_blizzards(turn)
            offsets = [(-1, 0), (1, 0), (0, 0), (0, -1), (0, 1)]
            row, col = position
            res = tuple([(row + d_row, col+ d_col) for d_row, d_col in offsets if self.can_move((row + d_row, col+ d_col), turn)])
            self.neighbors_cache[(position, turn)] = res
        return self.neighbors_cache[(position, turn)]

                    





def parse_input(input: str) -> str:
    board = [list(line.strip()) for line in input.strip().splitlines() if line.strip()]
    blizzards = []
    curr = None
    goal = None
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if curr is None and col == ".":
                curr = (i, j)
            if col == ".":
                goal = (i, j)
            if col in "^v<>":
                blizzards.append(Blizzard(col, {0: (i, j)}))
                board[i][j] = "."
      
    return Map(board, blizzards, curr, goal, {}, {}, {})

@lru_cache(maxsize=None)
def dist(pos1, pos2) -> int:
    r1, c1 = pos1
    r2, c2 = pos2
    return abs(r1-c1) + abs(r2-c2)
from queue import PriorityQueue

def solve(map: Map, start_turn: int = 0) -> int:
    queue = PriorityQueue()
    queue.put((dist(map.goal, map.curr),map.curr, start_turn))
    curr = map.curr
    max_turns = 0
    visited = set()
    queued = set()
    while queue:
        priority, curr, turns = queue.get()
        visited.add(curr + tuple(map.blizzard_positions(turns)))
        if priority > max_turns and priority % 5 == 0:
            info(f"expand horizon to {priority=}")
        max_turns = max(max_turns, priority)
        # debug(f"move to {curr} on {turns=}")
        if curr == map.goal:
            return turns
        for pos in map.neighbors(curr, turns + 1):
            key = (dist(map.goal, pos) + turns + 1, pos, turns + 1)
            if pos + tuple(map.blizzard_positions(turns + 1)) not in visited and key not in queued:
                queued.add(key)
                queue.put(key)

@timeit
def part1(map: Map) -> int:
    return solve(map)

@timeit
def part2(map: Map) -> int:
    there = solve(map)
    map = map.swap_goals()
    back = solve(map, there)
    map = map.swap_goals()
    info(f"{there=} {back=}")
    return solve(map, back)

stdin = sys.stdin.read()
input = parse_input(stdin)
test_input = parse_input(TEST_INPUT)
info("=" * 40)
# info(f"test 1: {part1(test_input)}")
# info(f"part 1: {part1(input)}")
input = parse_input(stdin)
test_input = parse_input(TEST_INPUT)
info(f"test 2: {part2(test_input)}")
info(f"part 2: {part2(input)}")