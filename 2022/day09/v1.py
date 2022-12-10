"""Day 9: Rope Bridge"""
import pathlib


def add(a, b):
    ax, ay = a
    bx, by = b
    return ax + bx, ay + by


def sub(a, b):
    ax, ay = a
    bx, by = b
    return ax - bx, ay - by


def rect_mag(a):
    ax, ay = a
    return max(abs(ax), abs(ay))


def rect_arg(a):
    def sgn(x):
        if x == 0:
            return 0
        return 1 if x > 0 else -1

    ax, ay = a
    return sgn(ax), sgn(ay)


def move_head(h, delta):
    h = add(h, delta)
    return h


def move_tail(h, t):
    d = sub(h, t)
    if rect_mag(d) <= 1:  # still touching
        return t
    t = add(t, rect_arg(d))
    return t


def move(h, t, delta):
    h = move_head(h, delta)
    t = move_tail(h, t)
    return h, t


def move_rope(ks, delta):
    ks[0] = move_head(ks[0], delta)
    for i in range(len(ks) - 1):
        ks[i + 1] = move_tail(ks[i], ks[i + 1])
    return ks


cmds = pathlib.Path("input.txt").read_text().splitlines()

head = (0, 0)
tail = (0, 0)
seen = {tail}

DELTA = dict(L=(-1, 0), R=(1, 0), U=(0, 1), D=(0, -1))

# print(" ", " ", head, tail)
for cmd in cmds:
    step_dir, step_cnt = cmd.split()
    for i in range(int(step_cnt)):
        head, tail = move(head, tail, DELTA[step_dir])
        seen.add(tail)
        # print(step_dir, i, head, tail)

# print(seen)
print("part 1:", len(seen))


knots = [(0, 0) for _ in range(10)]
seen2 = {(0, 0)}

# print(" ", " ", knots)
for cmd in cmds:
    step_dir, step_cnt = cmd.split()
    for i in range(int(step_cnt)):
        knots = move_rope(knots, DELTA[step_dir])
        seen2.add(knots[9])
        # print(step_dir, i, knots)

# print(seen2)
print("part 2:", len(seen2))
