range_pairs = []

class Range:
	def __init__(self, low, high):
		self.low = low
		self.high = high

	def contains(self, other: "Range") -> bool:
		return self.low >= other.low and self.high <= other.high

	def overlaps(self, other: "Range") -> bool:
		return self.contains(other) or other.contains(self) or other.low <= self.high <= other.high or other.low <= self.low <= other.high

with open('/tmp/advent-code-input-4') as f:
		raw_pairs = [l.strip().split(",") for l in f.readlines()]

def part_1():
	contain_count = 0
	for pair_1, pair_2 in raw_pairs:
		interval_1 = [int(limit) for limit in pair_1.split("-")]
		interval_2 = [int(limit) for limit in pair_2.split("-")]
		range_1 = Range(interval_1[0], interval_1[1])
		range_2 = Range(interval_2[0], interval_2[1])
		if range_1.contains(range_2) or range_2.contains(range_1):
			contain_count += 1
	print(contain_count)

contain_count = 0
for pair_1, pair_2 in raw_pairs:
	interval_1 = [int(limit) for limit in pair_1.split("-")]
	interval_2 = [int(limit) for limit in pair_2.split("-")]
	range_1 = Range(interval_1[0], interval_1[1])
	range_2 = Range(interval_2[0], interval_2[1])
	if range_1.overlaps(range_2):
		contain_count += 1
print(contain_count)