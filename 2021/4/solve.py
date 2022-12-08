import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from utils import *
from collections import *

TEST_INPUT = """
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
 
"""

PART_1_ANSWER = 0
PART_2_ANSWER = 0


def parse_input(input: str) -> str:
    return input.strip()


def part1(input: str) -> int:
    nums = [int(c) for c in input.splitlines()[0].strip().split(',')]
    boards = []
    board = []
    for line in input.splitlines()[2:]:
        line = line.strip()
        if not line and board:
            boards.append(board)
            board = []
        else:
            board.append([int(c) for c in line.split()])
    else:
        if board:
            boards.append(board)
    marked = [[[False for _ in row] for row in board] for board in boards]

    for num_num, num in enumerate(nums):
        for index, board in enumerate(boards):
            for row_num, row in enumerate(board):
                for col_num, col in enumerate(row):
                    if board[row_num][col_num] == num:
                        marked[index][row_num][col_num] = True
            for row in marked[index]:
                if all(row):
                    sum = 0
                    for row_num, row in enumerate(board):
                        for col_num, col in enumerate(row): 
                            if not marked[index][row_num][col_num]:
                                sum += board[row_num][col_num]
                    return sum * num

            for row in transpose(marked[index]):
                if all(row):
                    sum = 0
                    for row_num, row in enumerate(board):
                        for col_num, col in enumerate(row): 
                            if not marked[index][row_num][col_num]:
                                sum += board[row_num][col_num]
                    return sum * num
    return 0

def part2(input: str) -> int:
    nums = [int(c) for c in input.splitlines()[0].strip().split(',')]
    boards = []
    board = []
    for line in input.splitlines()[2:]:
        line = line.strip()
        if not line and board:
            boards.append(board)
            board = []
        else:
            board.append([int(c) for c in line.split()])
    else:
        if board:
            boards.append(board)
    marked = [[[False for _ in row] for row in board] for board in boards]
    has_won = set()
    for num_num, num in enumerate(nums):
        for index, board in enumerate(boards):
            for row_num, row in enumerate(board):
                for col_num, col in enumerate(row):
                    if board[row_num][col_num] == num:
                        marked[index][row_num][col_num] = True
            for row in marked[index]:
                if all(row):
                    has_won.add(index)
                    if len(has_won) == len(marked):
                        sum = 0
                        for row_num, row in enumerate(board):
                            for col_num, col in enumerate(row): 
                                if not marked[index][row_num][col_num]:
                                    sum += board[row_num][col_num]
                        return sum * num

            for row in transpose(marked[index]):
                if all(row):
                    has_won.add(index)
                    if len(has_won) == len(marked):
                        sum = 0
                        for row_num, row in enumerate(board):
                            for col_num, col in enumerate(row): 
                                if not marked[index][row_num][col_num]:
                                    sum += board[row_num][col_num]
                        return sum * num
    return 0


input = parse_input(sys.stdin.read())
test_input = parse_input(TEST_INPUT)
print("=" * 40)
print("test 1:", part1(test_input))
print("part 1:", part1(input))
print("test 2:", part2(test_input))
print("part 2:", part2(input))