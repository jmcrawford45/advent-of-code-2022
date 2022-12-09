import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from utils import *
from collections import *

TEST_INPUT = """
R 5
U 8
"""

PART_1_ANSWER = 13
PART_2_ANSWER = 0


def parse_input(input: str) -> str:
    return input.strip()

def should_move(p1: tuple[int, int], p2: tuple[int, int]):
    return abs(p1[0]-p2[0]) > 1 or abs(p1[1]-p2[1]) > 1


def part1(input: str) -> int:
    head = (0,0)
    tail = (0,0)
    seen = set([(0,0)])
    for line in input.splitlines():
        dir, val = line.strip().split()
        val = int(val)
        for _ in range(val):
            x,y = head
            if dir == "R":
                x += 1
            elif dir == "L":
                x -= 1
            elif dir == "U":
                y += 1
            else:
                y -= 1
            old_head = head
            head = (x,y)
            if should_move(head, tail):
                tail = old_head
                seen.add(old_head)
            
    return len(seen)

def part2(input: str) -> int:
    head = (0,0)
    tails = [(0,0)] * 9
    seen = set([(0,0)])
    for line in input.splitlines():
        dir, val = line.strip().split()
        val = int(val)
        for _ in range(val):
            x,y = head
            if dir == "R":
                x += 1
            elif dir == "L":
                x -= 1
            elif dir == "U":
                y += 1
            else:
                y -= 1
            old_head = head
            head = (x,y)
            for i, tail in enumerate(tails):
                if i == 0 and should_move(head, tail):
                    old_tail = tail
                    tails[i] = old_head
                    old_head = old_tail
                    print(f"move head tail to to {tails[i]}")
                elif i != len(tails) - 1 and should_move(tails[i-1], tail):
                    old_tail = tail
                    tails[i] = old_head
                    old_head = old_tail
                    print(f"move tail {i} to {tails[i]}")
                elif should_move(tails[i-1], tail):
                    print(f"move last tail to {tails[i]}")
                    old_tail = tail
                    tails[i] = old_head
                    old_head = old_tail
                    seen.add(old_head)
            
    return len(seen)


input = parse_input(sys.stdin.read())
test_input = parse_input(TEST_INPUT)
print("=" * 40)
print("test 1:", part1(test_input))
print("part 1:", part1(input))
print("test 2:", part2(test_input))
# print("part 2:", part2(input))