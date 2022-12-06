"""Day 1: Calorie Counting"""

with open("input.txt", "r") as f:
    lines = f.readlines()

calories = [0]

for line in lines:
    line = line.strip()
    if line:
        calories[-1] += int(line)
    else:
        calories.append(0)

# print(calories)
# print(len(calories))
print("part 1:", max(calories))

top_3 = sorted(calories)[-3:]
# print(top_3)
print("part 2:", sum(top_3))
