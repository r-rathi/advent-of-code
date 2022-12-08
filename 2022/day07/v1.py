"""Day 7: No Space Left On Device"""
import pathlib

lines = pathlib.Path("input.txt").read_text().splitlines()

cwd = None
dir_stack = []
dir_size = {}

for line in lines:
    parts = line.split()
    if parts[0] == "$":
        if parts[1] == "cd":
            dirname = parts[2]
            if dirname == "..":
                cwd_size = dir_size[cwd]
                dir_stack.pop()
                cwd = "/".join(dir_stack)
                dir_size[cwd] += cwd_size
            else:
                dir_stack.append(dirname)
                cwd = "/".join(dir_stack)
                dir_size[cwd] = 0
    elif parts[0] != "dir":
        dir_size[cwd] += int(parts[0])

# print(cwd)
# print(dir_stack)
# print(dir_size)

while dir_stack[-1] != "/":
    cwd_size = dir_size[cwd]
    dir_stack.pop()
    cwd = "/".join(dir_stack)
    dir_size[cwd] += cwd_size

# print(cwd)
# print(dir_stack)
# print(dir_size)

dirs_at_most_100k = {d: dir_size[d] for d in dir_size if dir_size[d] <= 100000}
# print(dirs_at_most_100k)

print("part 1:", sum(dirs_at_most_100k.values()))

DISK_SIZE = 70000000
NEED_SIZE = 30000000

used_size = dir_size["/"]
free_size = DISK_SIZE - used_size
min_delete_size = NEED_SIZE - free_size

# print("used_size:", used_size)
# print("free_size:", free_size)
# print("min_delete_size:", min_delete_size)

delete_candidates = {d: dir_size[d] for d in dir_size if dir_size[d] >= min_delete_size}
# print(delete_candidates)

sorted_delete_candidates = [(d, dir_size[d]) for d in sorted(delete_candidates, key=lambda d: dir_size[d])]
# print(sorted_delete_candidates)

delete_dir = sorted_delete_candidates[0][0]
print("part 2:", dir_size[delete_dir])

