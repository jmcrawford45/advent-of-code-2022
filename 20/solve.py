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
1
2
-3
3
-2
0
4
"""

PART_1_ANSWER = 3
PART_2_ANSWER = 0
from copy import deepcopy

class Node:
    def __init__(self, val):
        self.val = val
        self.next = None
        self.prev = None
    
    def __repr__(self):
        return f"Node({self.val=}, prev={self.prev.val}, next={self.next.val})"

def parse_input(input: str) -> tuple[Node, dict[int, Node]]:
    base = [int(c.strip()) for c in input.strip().splitlines()]
    head = curr = prev = Node(base[0])
    index = {0: head}
    for i, num in enumerate(base[1:]):
        curr.prev = prev
        curr.next = Node(num)
        index[i+1] = curr.next
        prev = curr
        curr = curr.next
    curr.prev = prev
    curr.next = head
    head.prev = curr
    curr = head.prev
    return (head, index)

def iterate(index):
    for i in sorted(index):
        if i % 500 == 499:
            info("500 processed")
        debug_node = index[0]
        node = index[i]
        to_move = node.val % len(index)
        if node.val < 0:
            to_move -= 1
        curr = node
        while to_move > 0:
            curr = curr.next
            to_move -= 1

        debug(f"{node} moves {node.val % len(index)} forward between {curr} and {curr.next}:")
        # insert and remove old pointers
        if curr != node:
            old_curr_next = curr.next
            old_curr_prev = curr.prev
            old_node_next = node.next
            old_node_prev = node.prev
            node.next = old_curr_next
            node.prev = curr
            curr.next = node
            old_node_next.prev = old_node_prev
            old_node_prev.next = old_node_next
            old_curr_next.prev = node
            old_curr_prev.next
            
        out = []
        for _ in range(len(index)):
            out.append(str(debug_node.val))
            debug_node = debug_node.next
        debug(' '.join(out))


def solve(input, rounds: int = 1) -> int:
    head, index = input
    for round_num in range(rounds):
        iterate(index)
        out = []
        debug_node = index[5]
        for _ in range(len(index)):
            out.append(str(debug_node.val))
            debug_node = debug_node.next
        info(f"After {round_num+1} round of mixing:")
        info(', '.join(out))
    curr = head
    while curr.val != 0:
        curr = curr.next
    steps = 3000
    result = 0
    for i in range(steps): 
        curr = curr.next
        if (i+1) % 1000 == 0:
            debug(f"add result {curr.val}")
            result += curr.val
    return result


@timeit
def part1(input: tuple[Node, dict[int, Node]]) -> int:
    return solve(input)

@timeit
def part2(input: str) -> int:
    _, index = input
    for i in index:
        index[i].val *= 811589153
    return solve(input, 10)


input = parse_input(sys.stdin.read())
test_input = parse_input(TEST_INPUT)
info("=" * 40)
info(f"test 1: {part1(test_input)}")
# info(f"part 1: {part1(input)}")
info(f"test 2: {part2(test_input)}")
# info(f"part 2: {part2(input)}")