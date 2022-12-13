import os
import sys
from logging import *
basicConfig(level=INFO)
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from utils import *
from collections import *
from functools import cmp_to_key

TEST_INPUT = """
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]

"""

PART_1_ANSWER = 0
PART_2_ANSWER = 0


def parse_input(input: str) -> list[Any]:
    pairs = []
    pair = []
    for line in input.strip().splitlines():
        if not line.strip():
            if pair:
                pairs.append(pair)
                pair = []
        else:
            pair.append(eval(line))
    if pair:
        pairs.append(pair)
    return pairs

def in_order_list(left: list[Any], right: list[Any]) -> bool:
    for i, val in enumerate(left):
        if i >= len(right):
            return False
        right_val = right[i]
        if isinstance(val, int) and isinstance(right_val, int):
            if right_val < val:
                return False
            elif right_val > val:
                return True
        elif isinstance(val, list) and isinstance(right_val, list):
            if in_order_list(val, right_val) is None:
                continue
            return in_order_list(val, right_val)
        elif isinstance(val, list):
            if in_order_list(val, [right_val]) is None:
                continue
            return in_order_list(val, [right_val])
        else:
            if in_order_list([val], right_val) is None:
                continue
            return in_order_list([val], right_val)
    if len(left) < len(right):
        return True 

def cmp_packets(left: list[Any], right: list[Any]) -> int:
    return 1 if in_order_list(left, right) else -1 


def part1(input: list[Any]) -> int:
    correct_order = []
    for i, pair in enumerate(input):
        left, right = pair
        if isinstance(left, int) and isinstance(right, list):
            left = [left]
        if isinstance(right, int) and isinstance(left, list):
            right = [right]
        if in_order_list(left, right):
            correct_order.append(i+1)
    debug(correct_order)
    return sum(correct_order)

def part2(input: list[Any]) -> int:
    all_packets = [[[2]], [[6]]]
    for left, right in input:
        all_packets.append(left)
        all_packets.append(right)
    all_packets.sort(key=cmp_to_key(cmp_packets), reverse=True)
    dividers = []
    for i, packet in enumerate(all_packets):
        if packet in [[[2]], [[6]]]:
            dividers.append(i+1)
    return dividers[0] * dividers[1]


input = parse_input(sys.stdin.read())
test_input = parse_input(TEST_INPUT)
info("=" * 40)
info(f"test 1: {part1(test_input)}")
info(f"part 1: {part1(input)}")
info(f"test 2: {part2(test_input)}")
info(f"part 2: {part2(input)}")