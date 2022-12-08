import os
import sys

TEST_INPUT = """
30373
25512
65332
33549
35390
"""

def parse_input(input: str) -> str:
    return input.strip()


def part1(input: str) -> int:
    trees = []
    visible = set()
    for line in input.splitlines():
        heights = [int(c) for c in line.strip()]
        trees.append(heights)
    # right
    for i, row in enumerate(trees):
        max_height = -1
        for j, tree in enumerate(row):
            if tree > max_height:
                max_height = tree
                visible.add((i,j))
    # left
    for i, row in enumerate(trees):
        max_height = -1
        for j, tree in reversed(list(enumerate(row))):
            if tree > max_height:
                max_height = tree
                visible.add((i,j))
    # down
    for i in range(len(trees[0])):
        max_height = -1
        for j in range(len(trees)):
            if trees[j][i] > max_height:
                visible.add((j, i))
                max_height = trees[j][i]

    # up
    for i in range(len(trees[0])):
        max_height = -1
        for j in reversed(range(len(trees))):
            if trees[j][i] > max_height:
                max_height = trees[j][i]
                visible.add((j, i))
    return len(visible)


def traverse(tree: int, trees: list[list[int]], point: tuple[int, int], offset: tuple[int, int]):
    visible = 0
    while True:
        point = (point[0] + offset[0], point[1] + offset[1])
        row, col  = point
        if not (0 <= row < len(trees)) or not (0 <= col < len(trees[0])):
            break
        if trees[point[0]][point[1]] >= tree:
            visible += 1
            break
        visible += 1
    return visible

def part2(input: str) -> int:
    trees = []
    visible = set()
    for line in input.splitlines():
        heights = [int(c) for c in line.strip()]
        trees.append(heights)
    max_score = -1
    for i, row in enumerate(trees):
        for j, tree in enumerate(row):
            base = 1
            for offset in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                base *= traverse(tree, trees, (i, j), offset)
            max_score = max(max_score, base)


    return max_score


input = parse_input(sys.stdin.read())
test_input = parse_input(TEST_INPUT)
print('=' * 40)
print("test 1:", part1(test_input))
print("part 1:", part1(input))
print("test 2:", part2(test_input))
print("part 2:", part2(input))
