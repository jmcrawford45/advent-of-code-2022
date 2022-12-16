import os
import sys
from logging import *
basicConfig(level=DEBUG)
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from utils import *
from collections import *

TEST_INPUT = """
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
"""

PART_1_ANSWER = 0
PART_2_ANSWER = 0

from dataclasses import *
from functools import lru_cache

@dataclass
class Valve:
    name: str
    flow_rate: int
    neighbors: list[str]

    def __hash__(self):
        return hash(self.name)

def parse_input(input: str) -> str:
    out = {}
    for line in input.strip().splitlines():
        start, end = line.split(";")
        name = start.split()[1]
        rate = int(start.split()[-1].split('=')[-1])
        neighbors = [end.split()[-1]]
        if 'valves' in end:
            neighbors = end.split(" valves ")[-1].split(', ')
        out[name] = Valve(name, rate, neighbors)
    return out


def part1(valves: dict[str, Valve]) -> int:
    @lru_cache(maxsize=None)
    def release_pressure(minutes_remaining: int, curr: Valve, open: tuple[str]) -> int:
        if minutes_remaining <= 1:
            return 0
        else:
            candidates = [
                release_pressure(minutes_remaining - 1, valves[neighbor], open) for neighbor in curr.neighbors
            ]
            if curr.name not in open and curr.flow_rate:
                candidates.append(curr.flow_rate * (minutes_remaining - 1) + release_pressure(minutes_remaining - 1, curr, open + (curr.name,)))
            return max(candidates)
    return release_pressure(30, valves["AA"], ())

def part2(valves: dict[str, Valve]) -> int:
    can_flow = list(sorted([v.name for v in valves.values() if v.flow_rate]))
    index_map = {name: index for index, name in enumerate(can_flow)}
    @lru_cache(maxsize=None)
    def release_pressure(minutes_remaining: int, curr: Valve, open: int) -> int:
        if minutes_remaining <= 1:
            return 0
        else:
            candidates = [
                release_pressure(minutes_remaining - 1, valves[neighbor], open) for neighbor in curr.neighbors
            ]
            if curr.name in index_map and not ((1 << index_map[curr.name])  & open):
                candidates.append(curr.flow_rate * (minutes_remaining - 1) + release_pressure(minutes_remaining - 1, curr, open + (1 << index_map[curr.name])))
            return max(candidates)
    res = 0
    for i in range(1 << (len(can_flow) - 1)):
        res = max(res, release_pressure(26, valves["AA"], i) + release_pressure(26, valves["AA"], i ^ ((1 << len(can_flow)) - 1)))
    return res


input = parse_input(sys.stdin.read())
test_input = parse_input(TEST_INPUT)
info("=" * 40)
info(f"test 1: {part1(test_input)}")
info(f"part 1: {part1(input)}")
info(f"test 2: {part2(test_input)}")
info(f"part 2: {part2(input)}")