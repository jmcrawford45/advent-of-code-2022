import os
import sys
from logging import *
basicConfig(level=INFO)
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from utils import *
from collections import *

TEST_INPUT = """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

PART_1_ANSWER = 0
PART_2_ANSWER = 0


def parse_input(input: str) -> str:
    paths = []
    for line in input.strip().splitlines():
        final = []
        path = [e.split(',') for e in line.strip().split(" -> ")]
        for point in path:
            final.append([int(coord) for coord in point])

        paths.append(final)
    return paths


def part1(input: list[list[int]]) -> int:
    occupied = set()
    max_depth = 0
    for path in input:
        prev = None
        for point in path:
            max_depth = max(max_depth, point[1])
            if prev is not None:
                if prev[0] == point[0]:
                    for y in range(min(prev[1], point[1]), max(prev[1], point[1]) + 1):
                        occupied.add((prev[0], y))
                else:
                    for x in range(min(prev[0], point[0]), max(prev[0], point[0]) + 1):
                        occupied.add((x, prev[1]))
            prev = point
    sand_fell = 0
    while True:
        sand = (500, 0)
        while sand[1] <= max_depth:
            if (sand[0], sand[1] + 1) in occupied and (sand[0] - 1, sand[1] + 1) in occupied and (sand[0] + 1, sand[1] + 1) in occupied:
                sand_fell += 1
                occupied.add(sand)
                break
            elif (sand[0], sand[1] + 1) not in occupied:
                sand = (sand[0], sand[1] + 1)
            elif (sand[0] - 1, sand[1] + 1) not in occupied:
                sand = (sand[0] - 1, sand[1] + 1)
            elif (sand[0] + 1, sand[1] + 1) not in occupied:
                sand = (sand[0] + 1, sand[1] + 1)
        if sand[1] >= max_depth or sand == (500, 0):
            return sand_fell


def part2(input: str) -> int:
    occupied = set()
    max_depth = 0
    min_x = None
    max_x = None
    for path in input:
        prev = None
        for point in path:
            if min_x is None:
                min_x = max_x = point[0]
            min_x = min(min_x, point[0])
            max_x = max(max_x, point[0])
            max_depth = max(max_depth, point[1])
            if prev is not None:
                if prev[0] == point[0]:
                    for y in range(min(prev[1], point[1]), max(prev[1], point[1]) + 1):
                        occupied.add((prev[0], y))
                else:
                    for x in range(min(prev[0], point[0]), max(prev[0], point[0]) + 1):
                        occupied.add((x, prev[1]))
            prev = point
    sand_fell = 0
    for x in range(-5 * min_x, 5 * max_x):
        occupied.add((x, max_depth + 2))
    while (500, 0) not in occupied:
        sand = (500, 0)
        while True:
            if (sand[0], sand[1] + 1) in occupied and (sand[0] - 1, sand[1] + 1) in occupied and (sand[0] + 1, sand[1] + 1) in occupied:
                if sand not in occupied:
                    sand_fell += 1
                    occupied.add(sand)
                break
            elif (sand[0], sand[1] + 1) not in occupied:
                sand = (sand[0], sand[1] + 1)
            elif (sand[0] - 1, sand[1] + 1) not in occupied:
                sand = (sand[0] - 1, sand[1] + 1)
            elif (sand[0] + 1, sand[1] + 1) not in occupied:
                sand = (sand[0] + 1, sand[1] + 1)
    return sand_fell


input = parse_input(sys.stdin.read())
test_input = parse_input(TEST_INPUT)
info("=" * 40)
info(f"test 1: {part1(test_input)}")
info(f"part 1: {part1(input)}")
info(f"test 2: {part2(test_input)}")
info(f"part 2: {part2(input)}")