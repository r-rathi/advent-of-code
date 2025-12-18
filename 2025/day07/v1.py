"""Day 7: Laboratories

Tags: #display #animation #colors
"""

import time

import matplotlib.colors as colors
import matplotlib.pyplot as plt

CLEAR_SCREEN = "\033[2J"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
FG_RED = "\033[31m"
FG_GREEN = "\033[32m"
FG_YELLOW = "\033[33m"
RESET = "\033[0m"


def display_manifold(manifold, splits):
    img = []
    for r, row in enumerate(manifold):
        img_row = []
        for c, char in enumerate(row):
            if char == "S":
                img_row.append(BG_YELLOW + "*" + RESET)
            if char == "o":
                img_row.append(FG_GREEN + "o" + RESET)
            elif char == "^":
                img_row.append(BG_RED + "^" + RESET)
            elif char == "|":
                img_row.append(FG_YELLOW + "|" + RESET)
            else:
                img_row.append(" ")
        img.append("".join(img_row))

    print(CLEAR_SCREEN)
    print("\n".join(img))
    print("splits:", splits)
    time.sleep(0.07)


def part1(lines, display=False):
    R = len(lines)
    C = len(lines[0])

    manifold = []
    for line in lines:
        row = list(line)
        row.append("")  # dummy column to eliminate bounday checks
        manifold.append(row)

    splits = 0
    if display:
        display_manifold(manifold, splits)

    beam = "S"
    for r in range(1, R):
        for c in range(C):
            if manifold[r][c] == "." and manifold[r - 1][c] == beam:
                manifold[r][c] = "|"
            elif manifold[r][c] == "^" and manifold[r - 1][c] == beam:
                manifold[r][c] = "o"
                manifold[r][c - 1] = "|"
                manifold[r][c + 1] = "|"
                splits += 1
        beam = "|"
        if display:
            display_manifold(manifold, splits)

    return splits


def part2(manifold, display=False):
    R, C = len(manifold), len(manifold[0])

    timelines = [[0] * (C + 1) for _ in range(R)]
    timelines[0][manifold[0].index("S")] = 1

    for r in range(1, R):
        for c in range(C):
            if manifold[r][c] == "^":
                timelines[r][c - 1] += timelines[r - 1][c]
                timelines[r][c + 1] += timelines[r - 1][c]
            else:
                timelines[r][c] += timelines[r - 1][c]

    if display:
        plt.imshow(timelines, norm=colors.LogNorm(), cmap="plasma")
        cbar = plt.colorbar()
        cbar.set_label("Number of timelines")
        plt.show()

    return sum(timelines[-1])


def main():
    # noinspection DuplicatedCode
    import argparse
    import pathlib

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    parser.add_argument("-d1", action="store_true", help="display part1")
    parser.add_argument("-d2", action="store_true", help="display part2")
    args = parser.parse_args()

    lines = pathlib.Path(args.f).read_text().splitlines()

    print("part 1:", part1(lines, display=args.d1))
    print("part 2:", part2(lines, display=args.d2))


if __name__ == "__main__":
    main()
