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
        msg = f' Took {total_time:.4f} seconds Function {func.__name__}{args} {kwargs}'[:1000]
        debug(msg)
        return result
    return timeit_wrapper


TEST_INPUT = """
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
"""

PART_1_ANSWER = 1000 * 6 + 4 * 8 + 0
PART_2_ANSWER = 0

@dataclass
class Map:
    map: list[list[StopIteration]]
    directions: list["Direction"]
    face_map: dict[(int, int, str), (int, int, str)]
    cube_len: int

@dataclass
class Direction:
    amount: int
    turn: int = 0

directions = [(0,1), (1, 0), (0, -1), (-1, 0)]

def cube_len(map: list[list[str]]) -> int:
    min_size = len(map[0])
    for row in map:
        min_size = min(min_size, len(row) - row.count(" "))
    return min_size

def parse_input(input: str) -> str:
    face_map = {}
    directions = input.strip().splitlines()[-1].strip()
    parsed_map = []
    max_len = 0
    for line in input.splitlines()[:-2]:
        max_len = max(max_len, len(line))
    for line in input.splitlines()[:-2]:
        if not (set(line) & set('.#')):
            continue
        parsed_map.append(list(line + ' ' * (max_len - len(line))))
    cube_size = cube_len(parsed_map)
    faces = "\n"
    face_coords = set()
    for face_row in range(len(parsed_map) // cube_size):
        for face_col in range(len(parsed_map[0]) // cube_size):
            if parsed_map[face_row * cube_size][face_col * cube_size] == " ":
                faces += "."
            else:
                faces += "#"
                face_coords.add((face_row, face_col))
                face_to_left = 0 <= face_col * cube_size - 1 and parsed_map[face_row * cube_size][face_col * cube_size - 1] != " "
                face_to_right = (face_col + 1) * cube_size < len(parsed_map[0]) and parsed_map[face_row * cube_size][(face_col + 1) * cube_size] != " "
                face_up = 0 <= face_row * cube_size - 1 and parsed_map[face_row * cube_size - 1][face_col * cube_size] != " "
                face_down = (face_row + 1) * cube_size < len(parsed_map) and parsed_map[(face_row + 1) * cube_size][face_col * cube_size] != " "
                if face_to_left:
                    # left
                    face_map[(face_row, face_col, "L")] = (face_row, face_col - 1, "L")
                if face_to_right:
                    # right
                    face_map[(face_row, face_col, "R")] = (face_row, face_col + 1, "R")
                if face_up:
                    # up
                    face_map[(face_row, face_col, "U")] = (face_row - 1, face_col, "U")
                if face_down:
                    # down
                    face_map[(face_row, face_col, "D")] = (face_row + 1, face_col, "D")
                if face_to_left and face_up:
                    face_map[(face_row, face_col - 1, "U")] = (face_row - 1, face_col, "R")
                    face_map[(face_row - 1, face_col, "L")] = (face_row, face_col - 1, "D")
                if face_to_left and face_down:
                    face_map[(face_row, face_col - 1, "D")] = (face_row + 1, face_col, "R")
                    face_map[(face_row + 1, face_col, "L")] = (face_row, face_col - 1, "U")
                if face_to_right and face_up:
                    face_map[(face_row, face_col + 1, "U")] = (face_row - 1, face_col, "L")
                    face_map[(face_row - 1, face_col, "R")] = (face_row, face_col + 1, "D")
                if face_to_right and face_down:
                    face_map[(face_row, face_col + 1, "D")] = (face_row + 1, face_col, "L")
                    face_map[(face_row + 1, face_col, "R")] = (face_row, face_col + 1, "U")




        faces += "\n"
    to_add = dict()
    combinations = set()
    possible_mappings = dict()
    while len(face_map) < 24:

        for x, y in face_map.items():
            cycle = [x, y]
            next_row, next_col, next_dir = y
            cycle_len = 2
            while (next_row, next_col, next_dir) in face_map and (next_row, next_col, next_dir) != cycle[0]:
                cycle_len += 1
                next_row, next_col, next_dir = face_map[next_row, next_col, next_dir]
                cycle.append((next_row, next_col, next_dir))
            if len(cycle) == 4:
                to_add[cycle[-1]] = cycle[0]
            elif len(cycle) == 3:
                for k, v in face_map.items():
                    if v == cycle[0]:
                        to_add[cycle[-1]] = k
        face_map.update(to_add)
        for row, col in face_coords:
            for dir in list("LRUD"):
                combinations.add((row, col, dir))
        for k in combinations - set(face_map):
            for v in combinations - set(face_map.values()):
                row,col,dir = k
                row2,col2,dir2 = v
                # cant have len 1 cycle
                if (row, col) != (row2, col2):
                    # cant have len 2 cycle or len 3 with identical dirs 
                    if abs(row-row2) + abs(col-col2) != 1 and dir != dir2:
                        debug("possible mapping")
                        possible_mappings[k] = v
        break

    face_map.update(possible_mappings)
    debug(faces)
    for k, v in sorted(face_map.items()):
        debug(f"{k}: {v}")




    num = ""
    parsed_dirs = []
    for char in directions:
        if "0" <= char <= "9":
            num += char
        elif char == "L":
            parsed_dirs.append(Direction(int(num), -1))
            num = ""
        elif char == "R":
            parsed_dirs.append(Direction(int(num), 1))
            num = ""
    if num:
        parsed_dirs.append(Direction(int(num)))

    return Map(parsed_map, parsed_dirs, face_map, cube_size)

directions = ["R", "D", "L", "U"]

@lru_cache(maxsize=None)
def _move(l: tuple[int], curr: int) -> int:
    if curr + 1 == len(l):
        try:
            next_wall = l.index("#")
        except ValueError:
            next_wall = -1
        try:
            next_space = l.index(".")
        except ValueError:
            next_space = -1
        if next_wall == -1 or (next_space >= 0 and next_space < next_wall):
            return next_space
        return curr
    else:
        next_space = curr + 1
        while l[next_space] == " ":
            next_space += 1
            next_space = next_space % len(l)
        if l[next_space] == ".":
            return next_space
        return curr

def move(l: Iterable[int], curr: int) -> int:
    return _move(tuple(l), curr)

transform_coords = {
    ("L", "L"): lambda row, col, cube_len: (row, cube_len - 1),
    ("L", "R"): lambda row, col, cube_len: (cube_len - row - 1, 0),
    ("L", "D"): lambda row, col, cube_len: (0, row),
    ("L", "U"): lambda row, col, cube_len: (cube_len - 1, cube_len - row - 1),
    ("R", "L"): lambda row, col, cube_len: (cube_len - row - 1, cube_len - 1),
    ("R", "R"): lambda row, col, cube_len: (row, 0),
    ("R", "D"): lambda row, col, cube_len: (0, cube_len - row - 1),
    ("R", "U"): lambda row, col, cube_len: (cube_len - 1, row),
    ("U", "L"): lambda row, col, cube_len: (cube_len - col - 1, cube_len - 1),
    ("U", "R"): lambda row, col, cube_len: (col, 0),
    ("U", "D"): lambda row, col, cube_len: (0, cube_len - col - 1),
    ("U", "U"): lambda row, col, cube_len: (cube_len - 1, col),
    ("D", "L"): lambda row, col, cube_len: (col, cube_len - 1),
    ("D", "R"): lambda row, col, cube_len: (cube_len - col - 1, 0),
    ("D", "D"): lambda row, col, cube_len: (0, col),
    ("D", "U"): lambda row, col, cube_len: (cube_len - 1, cube_len - col - 1),
}

def move2(position: tuple[int, int], input: Map, direction: str) -> tuple[int, int, str]:
    row, col = position
    off_left = direction == "L" and col % input.cube_len == 0
    off_right = direction == "R" and col % input.cube_len == input.cube_len - 1
    off_up = direction == "U" and row % input.cube_len == 0
    off_down = direction == "D" and row % input.cube_len == input.cube_len - 1
    if off_left or off_right or off_up or off_down:
        face_row, face_col, dir = input.face_map[(row // input.cube_len, col // input.cube_len, direction)]
        row_offset, col_offset = transform_coords[(direction, dir)](row % input.cube_len, col % input.cube_len, input.cube_len)
        if input.map[face_row * input.cube_len + row_offset][face_col * input.cube_len + col_offset] == "#":
            return (row, col, direction)
        return face_row * input.cube_len + row_offset, face_col * input.cube_len + col_offset, dir
        

    if direction == "L":
        candidate = (row, col-1, direction)
    elif direction == "R":
        candidate = (row, col+1, direction)
    elif direction == "U":
        candidate = (row-1, col, direction)
    elif direction == "D":
        candidate = (row+1, col, direction)
    if input.map[candidate[0]][candidate[1]] == "#":
        return (row, col, direction)
    return candidate


@timeit
def part1(input: Map) -> int:
    curr_row, curr_col = (0, input.map[0].index("."))
    debug(f"start at {(curr_row, curr_col)}")
    direction_mod = 0
    for direction in input.directions:
        moves_left = direction.amount
        debug(f"moving {direction}")
        while moves_left:
            moves_left -= 1
            curr_direction = directions[direction_mod % len(directions)]
            if curr_direction == "R":
                curr_col = move(input.map[curr_row], curr_col)
            elif curr_direction == "L":
                curr_col = len(input.map[curr_row]) - 1 - move(reversed(input.map[curr_row]), len(input.map[curr_row]) - 1 - curr_col)
            elif curr_direction == "D":
                curr_row = move((input.map[row][curr_col] for row in range(len(input.map))), curr_row)
            elif curr_direction == "U":
                curr_row = len(input.map) - 1 - move(reversed(tuple(input.map[row][curr_col] for row in range(len(input.map)))), len(input.map) - 1 - curr_row)
            debug(f"move to {(curr_row, curr_col)}")
        direction_mod += direction.turn
    curr_row += 1
    curr_col += 1  
    debug(f"end at {(curr_row, curr_col)}")      

            
    return 1000 * curr_row + 4 * curr_col + (direction_mod % len(directions))

@timeit
def part2(input: str) -> int:
    curr_row, curr_col = (0, input.map[0].index("."))
    debug(f"start at {(curr_row, curr_col)}")
    direction_mod = 0
    for direction in input.directions:
        moves_left = direction.amount
        debug(f"moving {direction}")
        while moves_left:
            moves_left -= 1
            curr_direction = directions[direction_mod % len(directions)]
            curr_row, curr_col, curr_direction = move2((curr_row, curr_col), input, curr_direction)
            direction_mod = directions.index(curr_direction)
            debug(f"move to {(curr_row, curr_col)}")
        direction_mod += direction.turn
    curr_row += 1
    curr_col += 1  
    debug(f"end at {(curr_row, curr_col)}")      

            
    return 1000 * curr_row + 4 * curr_col + (direction_mod % len(directions))

test_input = parse_input(TEST_INPUT)
input = parse_input(sys.stdin.read())
info("=" * 40)
info(f"test 1: {part1(test_input)}")
info(f"part 1: {part1(input)}")
info(f"test 2: {part2(test_input)}")
info(f"part 2: {part2(input)}")