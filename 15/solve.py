import os
import sys
from logging import *
basicConfig(level=INFO)
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from utils import *
from collections import *
from dataclasses import *

TEST_INPUT = """
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""

PART_1_ANSWER = 0
PART_2_ANSWER = 0


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

@dataclass
class Entry:
    sensor: Point
    beacon: Point

def parse_input(input: str) -> list[Entry]:
    locs = []
    for line in input.strip().splitlines():
        sensor, beacon = line.split(": ")
        sensor_x, sensor_y = sensor.split()[-2:]
        sensor = Point(int(sensor_x.split("x=")[-1].strip(",")), int(sensor_y.split("y=")[-1]))
        beacon_x, beacon_y = beacon.split()[-2:]
        beacon = Point(int(beacon_x.split("x=")[-1].strip(",")), int(beacon_y.split("y=")[-1]))
        locs.append(Entry(sensor, beacon))
    return locs

def distance(p1: Point, p2: Point) -> int:
    return abs(p1.x-p2.x) + abs(p1.y-p2.y)



def part1(input: list[Entry], row: int) -> int:
    beacon_locs = set()
    for entry in input:
        if entry.beacon.y == row:
            beacon_locs.add(entry.beacon.x)

    no_beacon_locs = set()
    for entry in input:
        dist = distance(entry.sensor, entry.beacon)
        dist_to_row = distance(entry.sensor, Point(entry.sensor.x, row))
        for offset in range((dist - dist_to_row) + 1):
            no_beacon_locs.add(entry.sensor.x + offset)
            no_beacon_locs.add(entry.sensor.x - offset)
    no_beacon_locs -= beacon_locs
    return len(no_beacon_locs)

def part2(input, bounds: int) -> int:
    candidates = set()
    occupied = set()
    for entry in input:
        if len(candidates) == 1:
            debug(list(candidates)[0].x * 4000000 + list(candidates)[0].y)
        occupied |= {entry.sensor, entry.beacon}
        dist = distance(entry.sensor, entry.beacon)
        candidate_locs = set()
        for x_offset in range(dist + 2):
            y_offset = dist - x_offset + 1
            candidate_locs |= {
                Point(entry.sensor.x + x_offset, entry.sensor.y + y_offset),
                Point(entry.sensor.x + x_offset, entry.sensor.y - y_offset),
                Point(entry.sensor.x - x_offset, entry.sensor.y + y_offset),
                Point(entry.sensor.x - x_offset, entry.sensor.y - y_offset)
            }
            candidate_locs = {p for p in candidate_locs - occupied if 0 <= p.x <= bounds and 0 <= p.y <= bounds}
            to_remove = set()
            for candidate in candidate_locs:
                for entry2 in input:
                    if distance(candidate, entry2.sensor) <= distance(entry2.sensor, entry2.beacon):
                            to_remove.add(candidate)
                            break
            candidate_locs -= to_remove

        candidates |= candidate_locs - occupied
    if len(candidates) == 1:
        return list(candidates)[0].x * 4000000 + list(candidates)[0].y


input = parse_input(sys.stdin.read())
test_input = parse_input(TEST_INPUT)
info("=" * 40)
info(f"test 1: {part1(test_input, 10)}")
info(f"part 1: {part1(input, 2000000)}")
info(f"test 2: {part2(test_input, 20)}")
info(f"part 2: {part2(input, 4000000)}")