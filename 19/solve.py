import os
import sys
from logging import *
basicConfig(level=DEBUG)
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from utils import *
from collections import *
from functools import lru_cache
from dataclasses import dataclass


TEST_INPUT = """
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.

  """

PART_1_ANSWER = 0
PART_2_ANSWER = 0


@dataclass
class Cost:
    amount: int
    kind: str
    def __hash__(self) -> int:
        return self.hash

@dataclass
class Robot:
    kind: str
    costs: tuple[Cost]

    def __hash__(self) -> int:
        return hash(self.kind) + hash(self.costs)



@dataclass
class RobotCostTuple:
    kind: str
    costs: tuple[Cost]

    def __hash__(self) -> int:
        return hash(self.kind) + hash(self.costs)
    
    @lru_cache(maxsize=None)
    def can_build(self, resources: tuple[int]) -> bool:
        return all(a >= b for a, b in zip(resources, self.costs))


@dataclass
class Blueprint:
    robots: tuple[Robot] = None
    def __hash__(self):
        return hash(self.robots)

class FrozenDict(OrderedDict):
    def __hash__(self):
        return hash(self.items())

@dataclass
class Input:
    blueprints: tuple[Blueprint]
    def costs(self):
        blueprints_costs = []
        for blueprint in self.blueprints:
            blueprint_costs = []
            for robot in blueprint.robots:
                costs = [0] * len(ore_index)
                for cost in robot.costs:
                    costs[ore_index[cost.kind]] += cost.amount
                blueprint_costs.append(RobotCostTuple(robot.kind, tuple(costs)))
            blueprints_costs.append(tuple(blueprint_costs))
        return tuple(blueprints_costs)
    
    def max_robots(self):
        max_robots = []
        for blueprint in self.blueprints:
            max_usage = defaultdict(int)
            for robot in blueprint.robots:
                for cost in robot.costs:
                    max_usage[cost.kind] = max(max_usage[cost.kind], cost.amount)
            max_per_blueprint = [1000] * len(ore_index)
            for val, idx in ore_index.items():
                max_per_blueprint[idx] = max_usage[val]
            max_robots.append(tuple(max_per_blueprint))
        return max_robots

ore_index: FrozenDict[str, int] = FrozenDict({"ore": 0, "clay": 1, "obsidian": 2, "geode": 3})

def parse_input(input: str) -> list[Input]:
    blueprints = []
    for line in input.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        costs = line.split(': ')[1]
        robots = []
        for robot in costs.split('. '):
            desc, cost = robot.split(" costs ")
            kind = desc.split()[1]
            costs  = cost.strip().split(" and ")
            costs = [Cost(int(c.strip().split()[0]), c.strip().split()[1].rstrip(".")) for c in costs]
            robots.append(Robot(kind, tuple(costs)))
        blueprints.append(Blueprint(robots))
    return Input(tuple(blueprints))


def collect_geodes(blueprint_idx: int, minutes_remaining: int, robot_cap: tuple[int], blueprints_costs: tuple[tuple[RobotCostTuple]]) -> int:


    def _collect_geodes(minutes_remaining: int):
        dp = set()
        queue = deque()
        queue.append((0, 0, 0, 0, 1, 0, 0, 0, minutes_remaining))
        max_collected = 0
        while queue:
            state = queue.pop()
            ore, clay, obsidian, geodes, rateOre, rateClay, rateObsidian, rateGeode, minutes_remaining = state
            max_collected = max(max_collected, geodes)
            if minutes_remaining == 0:
                continue

            maxCostOre, maxCostClay, maxCostObsidian, _ = robot_cap
            rateOre = min(rateOre, maxCostOre)
            rateClay = min(rateClay, maxCostClay)
            rateObsidian = min(rateObsidian, maxCostObsidian)
            ore = min(ore, minutes_remaining * maxCostOre - rateOre * (minutes_remaining - 1))
            clay = min(clay, minutes_remaining * maxCostClay - rateClay * (minutes_remaining - 1))
            obsidian = min(obsidian, minutes_remaining * maxCostObsidian - rateObsidian * (minutes_remaining - 1))
            key = (ore, clay, obsidian, geodes, rateOre, rateClay, rateObsidian, rateGeode, minutes_remaining)
            robots = (rateOre, rateClay, rateObsidian, rateGeode)
            if key in dp:
                continue
            dp.add(key)
            for robot in blueprints_costs[blueprint_idx]:
                costs = robot.costs
                if robot.can_build((ore, clay, obsidian, geodes)):
                    next_robots = tuple(a if i != ore_index[robot.kind] else a+1 for i,a in enumerate(robots))
                    next_resources = tuple(a+b-c for a,b,c in zip((rateOre, rateClay, rateObsidian, rateGeode), (ore, clay, obsidian, geodes), costs))
                    queue.append(next_resources + next_robots + (minutes_remaining - 1,))
            next_resources = (ore + rateOre, clay + rateClay, obsidian + rateObsidian, geodes + rateGeode)
            queue.append(next_resources + robots + (minutes_remaining - 1,))
        return max_collected
    return _collect_geodes(minutes_remaining)


def part1(input: Input) -> int:
    blueprints_costs = input.costs()
    max_robots = input.max_robots()

    result = 0
    for i in range(len(input.blueprints)):
        result += (i+1) * collect_geodes(i, 24, max_robots[i], blueprints_costs)
    return result

def part2(input: Input) -> int:
    blueprints_costs = input.costs()
    max_robots = input.max_robots()

    result = 1
    for i in range(len(input.blueprints[:3])):
        geodes_collected = collect_geodes(i, 32, max_robots[i], blueprints_costs)
        debug(f"{i=} {geodes_collected=}")
        result *= geodes_collected
    return result


input = parse_input(sys.stdin.read())
test_input = parse_input(TEST_INPUT)
info("=" * 40)
info(f"test 1: {part1(test_input)}")
info(f"part 1: {part1(input)}")
info(f"test 2: {part2(test_input)}")
info(f"part 2: {part2(input)}")