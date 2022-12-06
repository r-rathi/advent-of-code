"""Day 3: Rucksack Reorganization"""

import pathlib
import string

priority = {c: (i + 1) for i, c in enumerate(string.ascii_letters)}

items = pathlib.Path("input.txt").read_text().split()
shared = [
    (set(item[: len(item) // 2]) & set(item[len(item) // 2:])).pop() for item in items
]
shared_priorities = [priority[item] for item in shared]
# print(shared_priorities)
print("part 1:", sum(shared_priorities))

groups = [items[i: i + 3] for i in range(0, len(items), 3)]
badges = [(set(group[0]) & set(group[1]) & set(group[2])).pop() for group in groups]
badge_priorities = [priority[badge] for badge in badges]
# print(badges)
# print(badge_priorities)
print("part 2:", sum(badge_priorities))
