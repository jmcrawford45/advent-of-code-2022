with open('/tmp/advent-code-input-3') as f:
		sacks = [l.strip() for l in f.readlines()]

def part_1():
	priorities = 0
	for sack in sacks:
		item_in_both = ''.join(set(sack[:len(sack)//2]) & set(sack[len(sack)//2:]))
		priorities += 1 + ord(item_in_both) - ord("a") if "a" <= item_in_both <= "z" else 27 + ord(item_in_both) - ord("A")
	print(priorities)	

priorities = 0
for group_num in range(len(sacks)//3):
	group = sacks[group_num*3:group_num*3+3]
	common_item = ''.join(set(group[0]) & set(group[1]) & set(group[2]))
	priorities += 1 + ord(common_item) - ord("a") if "a" <= common_item <= "z" else 27 + ord(common_item) - ord("A")
print(priorities)