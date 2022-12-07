with open('/tmp/advent-code-input-6') as f:
	stream = f.read().strip()

for index in range(len(stream) - 14):
	if len(set(stream[index:index+14])) == 14:
		print(index + 14)
		break

