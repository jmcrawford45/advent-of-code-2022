with open('/tmp/advent-code-input-1') as f:
		nums = [l.strip() for l in f.readlines()]

def part_1():
	max_calories = curr_calories = 0
	for num in nums:
		if not num:
			max_calories = max(max_calories, curr_calories)
			curr_calories = 0
		else:
			curr_calories += int(num)
	max_calories = max(max_calories, curr_calories)
	print(max_calories)


curr_calories = 0
calories = []
for num in nums:
	if not num:
		calories.append(curr_calories)
		curr_calories = 0
	else:
		curr_calories += int(num)
if num:
	calories.append(curr_calories)
print(sum(list(reversed(sorted(calories)))[:3]))