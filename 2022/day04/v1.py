"""Day 4: Camp Cleanup"""
import pathlib

input_lines = pathlib.Path("input.txt").read_text().splitlines()
range_pairs = [line.split(",") for line in input_lines]

contained = 0
overlaps = 0

for pair in range_pairs:
    l0, r0 = [int(x) for x in pair[0].split("-")]
    l1, r1 = [int(x) for x in pair[1].split("-")]
    if (l0 <= l1 and r0 >= r1) or (l1 <= l0 and r1 >= r0):
        contained += 1
    if (l1 <= r0) and (l0 <= r1):
        overlaps += 1

print("part 1:", contained)
print("part 2:", overlaps)
