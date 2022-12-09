import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from utils import *
from collections import *

TEST_INPUT = """
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""

PART_1_ANSWER = 13
PART_2_ANSWER = 36


def parse_input(input: str) -> str:
    return input.strip()

def should_move(p1: tuple[int, int], p2: tuple[int, int]):
    return abs(p1[0]-p2[0]) > 1 or abs(p1[1]-p2[1]) > 1

def get_move(p1: tuple[int, int], p2: tuple[int, int]):
    x = p1[0] - p2[0]
    if x <= -1:
        x = -1
    elif x >= 1:
        x = 1
    y = p1[1] - p2[1]
    if y <= -1:
        y = -1
    elif y >= 1:
        y = 1
    return (x, y)




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
            head = (x,y)
            new_tails = []
            if should_move(head, tails[0]):
                move = get_move(head, tails[0])
                new_tails.append((tails[0][0] + move[0], tails[0][1] + move[1]))
                for i in range(1, len(tails)):
                    if should_move(new_tails[i-1], tails[i]):
                        move = get_move(new_tails[i-1], tails[i])
                        new_tails.append((tails[i][0] + move[0], tails[i][1] + move[1]))
                        if i == len(tails) - 1:
                            seen.add(tails[i])
                    else:
                        new_tails.append(tails[i])
                tails = new_tails
        # base = [["."] * 10 for _ in range(10)]
        # base[head[0]][head[1]] = "H"
        # for i, tail in enumerate(tails):
        #     if base[tail[0]][tail[1]] == ".":
        #         base[tail[0]][tail[1]] = str(i+1)
        # print("-" * 40)
        # base = transpose(base)
        # for row in reversed(base):
        #     print(" ".join(row))
            
    return len(seen) + 1


input = parse_input(sys.stdin.read())
test_input = parse_input(TEST_INPUT)
print("=" * 40)
print("test 1:", part1(test_input))
print("part 1:", part1(input))
print("test 2:", part2(test_input))
print("part 2:", part2(input))