TEST_INPUT = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
""".splitlines()

from collections import defaultdict
curr_dirr = ""
sizes = defaultdict(int)
subdirs = defaultdict(set)
seen_files = set()
for line in TEST_INPUT:
	if line.startswith("$ cd"):
		if not ".." in line:
			curr_dirr += f"{line.strip().split()[-1]}" if not curr_dirr else f"/{line.strip().split()[-1]}"
		else:
			curr_dirr = "/".join(curr_dirr.split("/")[:-1])
	elif not line.startswith("$ ls") and not line.startswith('dir'):
		size = int(line.strip().split()[0])
		if f"{curr_dirr}/{line.strip().split()[1]}" not in seen_files:
			sizes[curr_dirr.lstrip("/")] += size
	elif line.startswith('dir'):
		subdirs[curr_dirr.lstrip('/')].add(line.strip().split()[-1])
USED = sum(sizes.values())
order = list(subdirs.keys())
order.sort(key=lambda x: x.count("/"), reverse=True)
for curr_dirr in order:
	for subdir in subdirs[curr_dirr]:
		sizes[curr_dirr] += sizes[f"{curr_dirr}/{subdir}".lstrip("/")] 
part_1 = sum(size for curr_dirr, size in sizes.items() if size <= 100000)
print(f"{part_1=}")

NEEDED = 30000000
TOTAL_SIZE = 70000000
AVAILABLE = TOTAL_SIZE - USED
print(f"{AVAILABLE=}")
print(f"{USED=}")
part_2 = min((size, curr_dirr) for curr_dirr, size in sizes.items() if AVAILABLE + size >= NEEDED)
print(f"{part_2=}")

