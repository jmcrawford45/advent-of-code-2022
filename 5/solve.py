"""
                    [Q]     [P] [P]
                [G] [V] [S] [Z] [F]
            [W] [V] [F] [Z] [W] [Q]
        [V] [T] [N] [J] [W] [B] [W]
    [Z] [L] [V] [B] [C] [R] [N] [M]
[C] [W] [R] [H] [H] [P] [T] [M] [B]
[Q] [Q] [M] [Z] [Z] [N] [G] [G] [J]
[B] [R] [B] [C] [D] [H] [D] [C] [N]
 1   2   3   4   5   6   7   8   9 
 """
STACKS = {
	1: list("BQC"),
	2: list("RQWZ"),
	3: list("BMRLV"),
	4: list("CZHVTW"),
	5: list("DZHBNVG"),
	6: list("HNPCJFVQ"),
	7: list("DGTRWZS"),
	8: list("CGMNBWZP"),
	9: list("NJBMWQFP"),
	# 1: list("ZN"),
	# 2: list("MCD"),
	# 3: list("P"),
} 
moves = []

with open('/tmp/advent-code-input-5') as f:
	for line in f:
		l = line.strip().split()
		amount, from_stack, to_stack = int(l[1]), int(l[3]), int(l[5])
		moves.append((amount, from_stack, to_stack))


def part_1():
	for amount, from_stack, to_stack in moves:
		for _ in range(amount):
			STACKS[to_stack].append(STACKS[from_stack].pop())
	print(''.join(s[-1] for s in STACKS.values()))

# print(f"{moves=}")
for amount, from_stack, to_stack in moves:
	# print(f"old {STACKS=}")
	# print(f"{amount=}, {from_stack=}, {to_stack=}")
	moved = STACKS[from_stack][-1 * amount:]
	STACKS[from_stack] = list(STACKS[from_stack][:amount * -1])
	STACKS[to_stack].extend(moved) 
	# print(f"new {STACKS=}")
print(''.join(s[-1] for s in STACKS.values()))