"""Day 10: Cathode-Ray Tube"""
import pathlib

lines = pathlib.Path("input.txt").read_text().splitlines()

imem = []
for line in lines:
    inst = line.split()
    if inst[0] == "noop":
        imem.append((inst[0], 0))
    else:
        imem.append((inst[0], int(inst[1])))

cycle = 1
FEX, EX1 = 0, 1
state = FEX
x = 1
pc = 0

cycle_x = []

while True:
    op, arg = imem[pc]

    cycle_x.append([cycle, x])
    # print(f"{cycle:3d} {x:>4} {cycle * x}", pc, op, arg)

    if state == FEX:
        next_state = FEX if op == "noop" else EX1
    else:
        next_state = FEX

    if next_state == FEX:
        pc += 1

    if state == EX1 and next_state == FEX:
        x += arg

    if pc == len(imem):
        break

    state = next_state
    cycle += 1

cycle_x.append([cycle, x])
# print(f"{cycle:3d} {x:>4} {cycle * x}", pc, op, arg)

signal_strength = sum(c * x for c, x in cycle_x if (c - 20) % 40 == 0)
print("part 1:", signal_strength)


class CRT:
    def __init__(self, width, height, fill_value="x"):
        self.buf = [[fill_value] * width for _ in range(height)]

    def render(self):
        return "\n".join(["".join(row) for row in self.buf])


crt = CRT(width=40, height=6)

for cycle, x in cycle_x:
    r = (cycle - 1) // 40
    c = (cycle - 1) % 40
    # print(cycle, r, c, x)
    crt.buf[r][c] = "#" if c in [x - 1, x, x + 1] else "."

print("part 2:")
print(crt.render())
