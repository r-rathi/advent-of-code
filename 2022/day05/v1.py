"""Day 5: Supply Stacks"""
import copy
import pathlib

input_lines = pathlib.Path("input.txt").read_text().splitlines()

stack_lines = []
moves = []
stack_lines_done = False

for line in input_lines:
    if not line.strip():
        stack_lines_done = True
        continue

    if not stack_lines_done:
        stack_lines.append(line)
    else:
        _, cnt, _, src, _, dst = line.split()
        moves.append((int(cnt), src, dst))


stack_labels = stack_lines.pop().split()
stacks = {label: [] for label in stack_labels}

for line in reversed(stack_lines):
    row = [line[i] for i in range(1, len(line), 4)]
    assert len(stack_labels) == len(row)
    # print(row)
    for label, crate in zip(stack_labels, row):
        if not crate.isspace():
            stacks[label].append(crate)

# for k, v in stacks.items(): print(f"{k}: {v}")

stacks2 = copy.deepcopy(stacks)


def kpop(stack, k):
    items = stack[-k:]
    del stack[-k:]
    return items


def kpush(stack, items):
    stack.extend(items)


for cnt, src, dst in moves:
    # part 1: one at a time
    for _ in range(cnt):
        kpush(stacks[dst], kpop(stacks[src], 1))
    # part 2: k at a time
    kpush(stacks2[dst], kpop(stacks2[src], cnt))

# for k, v in stacks.items(): print(f"{k}: {v}")
# for k, v in stacks2.items(): print(f"{k}: {v}")

top_crates1 = [stack[-1] for stack in stacks.values()]
top_crates2 = [stack[-1] for stack in stacks2.values()]

print("part 1:", "".join(top_crates1))
print("part 2:", "".join(top_crates2))
