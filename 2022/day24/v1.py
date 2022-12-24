"""Day 24: Blizzard Basin"""
import argparse
import pathlib
import time
from itertools import count


def trek(valley, R, C, start, goal, display):
    expedition = {start}
    for t in count(0):
        if display:
            render(valley, expedition, R, C, header=f"{t=}\n")
            time.sleep(1/30)

        if goal in expedition:
            return t, valley

        valley = blizzard_step(valley, R, C)
        expedition = expedition_step(valley, expedition, R, C)

    return None, None


def render(valley, expedition, R, C, header=""):
    CLEAR_SCREEN = "\033[2J"
    FG_GREEN = "\033[32m"
    RESET = "\033[0m"
    E = FG_GREEN + "E" + RESET

    img = []
    for r in range(R):
        for c in range(C):
            v = valley[(r, c)]
            assert (r, c) not in expedition or not v, ((r, c), v, expedition)
            if len(v) == 0:
                img.append(E if (r, c) in expedition else ".")
            elif len(v) == 1:
                img.append(v[0])
            else:
                img.append(str(len(v)))
        img.append("\n")
    print(CLEAR_SCREEN + header + "".join(img))


def blizzard_step(valley, R, C):
    next_valley = {}
    for r in range(R):
        for c in range(C):
            if 0 < r < R - 1 and 0 < c < C - 1:
                next_valley[(r, c)] = []
            else:
                next_valley[(r, c)] = valley[(r, c)]

    for r in range(1, R - 1):
        for c in range(1, C - 1):
            for b in valley[(r, c)]:
                if b == "^":
                    r_next = R - 2 if r == 1 else r - 1
                    next_valley[(r_next, c)].append(b)
                elif b == "v":
                    r_next = 1 if r == R - 2 else r + 1
                    next_valley[(r_next, c)].append(b)
                elif b == "<":
                    c_next = C - 2 if c == 1 else c - 1
                    next_valley[(r, c_next)].append(b)
                elif b == ">":
                    c_next = 1 if c == C - 2 else c + 1
                    next_valley[(r, c_next)].append(b)

    return next_valley


def expedition_step(valley, expedition, R, C):
    next_expedition = set()
    for r, c in expedition:
        for dr, dc in ((0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and not valley[(nr, nc)]:
                next_expedition.add((nr, nc))
    return next_expedition


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", default="input.txt", help="input txt file (default: input.txt)"
    )
    parser.add_argument("-d", action="store_true", help="display")
    args = parser.parse_args()

    lines = pathlib.Path(args.f).read_text().splitlines()

    R, C = len(lines), len(lines[0])
    valley0 = {}
    for r in range(R):
        for c in range(C):
            blizzard = lines[r][c]
            valley0[(r, c)] = [] if blizzard == "." else [blizzard]

    start = 0, lines[0].index(".")
    goal = R - 1, lines[R - 1].index(".")

    t1, valley1 = trek(valley0, R, C, start=start, goal=goal, display=args.d)
    t2, valley2 = trek(valley1, R, C, start=goal, goal=start, display=args.d)
    t3, valley3 = trek(valley2, R, C, start=start, goal=goal, display=args.d)
    print("times:", t1, t2, t3)
    print("part 1:", t1)
    print("part 2:", t1 + t2 + t3)


if __name__ == "__main__":
    main()
