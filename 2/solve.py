with open('/tmp/advent-code-input-2') as f:
		plays = [l.strip().split() for l in f.readlines()]

def part_1():
	MAPPING = {
		# rock = 1, paper = 2, scissors = 3
		"A": 1,
		"B": 2,
		"C": 3,
		"X": 1,
		"Y": 2,
		"Z": 3
	}

	def outcome_score(their_play: str, our_play: str) -> int:
		"""Win = 6, draw = 3, loss = 0"""
		if MAPPING[their_play] == MAPPING[our_play]:
			return 3
		if abs(MAPPING[their_play] - MAPPING[our_play]) == 1:
			return 6 if MAPPING[our_play] > MAPPING[their_play] else 0
		return 0 if MAPPING[our_play] > MAPPING[their_play] else 6
		

	def score_play(their_play: str, our_play: str) -> int:
		play_score = MAPPING[our_play]
		return play_score + outcome_score(their_play, our_play)

	total = 0
	for their_play, our_play in plays:
		total += score_play(their_play, our_play)
	print(total)

MAPPING = {
		# rock = 1, paper = 2, scissors = 3
		# outcome + val
		("A", "X"): 0 + 3,
		("A", "Y"): 3 + 1,
		("A", "Z"): 6 + 2,
		("B", "X"): 0 + 1,
		("B", "Y"): 3 + 2,
		("B", "Z"): 6 + 3,
		("C", "X"): 0 + 2,
		("C", "Y"): 3 + 3,
		("C", "Z"): 6 + 1,
	}



total = 0
for their_play, outcome in plays:
	total += MAPPING[(their_play, outcome)]
print(total)
