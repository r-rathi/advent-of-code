"""Day 14: Parabolic Reflector Dish"""

import argparse
import copy
import pathlib


def render(platform):
    return "\n".join("".join(rock for rock in row) for row in platform)


def load(platform: list[list[str]]) -> int:
    R = len(platform)
    return sum(row.count("O") * (R - r) for r, row in enumerate(platform))


def tilt_north(platform):
    R, C = len(platform), len(platform[0])
    moved = True
    iteration = 0
    while moved:
        moved = False
        # print(f"{iteration=}\n{render(platform)}")
        for r in range(1, R):
            for c in range(C):
                if platform[r][c] == "O" and platform[r - 1][c] == ".":
                    platform[r - 1][c] = "O"
                    platform[r][c] = "."
                    moved = True
        iteration += 1
    # print(f"{iteration=}\n{render(platform)}")


def tilt_west(platform):
    R, C = len(platform), len(platform[0])
    moved = True
    iteration = 0
    while moved:
        moved = False
        # print(f"{iteration=}\n{render(platform)}")
        for c in range(1, C):
            for r in range(R):
                if platform[r][c] == "O" and platform[r][c - 1] == ".":
                    platform[r][c - 1] = "O"
                    platform[r][c] = "."
                    moved = True
        iteration += 1
    # print(f"{iteration=}\n{render(platform)}")


def tilt_south(platform):
    R, C = len(platform), len(platform[0])
    moved = True
    iteration = 0
    while moved:
        moved = False
        # print(f"{iteration=}\n{render(platform)}")
        for r in range(R - 2, -1, -1):
            for c in range(C):
                if platform[r][c] == "O" and platform[r + 1][c] == ".":
                    platform[r + 1][c] = "O"
                    platform[r][c] = "."
                    moved = True
        iteration += 1
    # print(f"{iteration=}\n{render(platform)}")


def tilt_east(platform):
    R, C = len(platform), len(platform[0])
    moved = True
    iteration = 0
    while moved:
        moved = False
        # print(f"{iteration=}\n{render(platform)}")
        for c in range(C - 2, -1, -1):
            for r in range(R):
                if platform[r][c] == "O" and platform[r][c + 1] == ".":
                    platform[r][c + 1] = "O"
                    platform[r][c] = "."
                    moved = True
        iteration += 1
    # print(f"{iteration=}\n{render(platform)}")


def part1(platform: list[list[str]]):
    tilt_north(platform)
    return load(platform)


def part2(platform: list[list[str]], cycles):
    R, C = len(platform), len(platform[0])

    state = tuple((r, c) for r in range(R) for c in range(C) if platform[r][c] == "O")

    states = {state: 0}
    found_loop = False
    target = cycles
    for cycle in range(1, cycles + 1):
        tilt_north(platform)
        tilt_west(platform)
        tilt_south(platform)
        tilt_east(platform)

        state = tuple(
            (r, c) for r in range(R) for c in range(C) if platform[r][c] == "O"
        )

        if not found_loop and state in states:
            found_loop = True
            offset = states[state]
            period = cycle - offset
            target = (cycles - offset) % period + cycle
            # print(f"found loop at {cycle=}, {offset=} {period=} {target=}")

        if cycle == target:
            break

        states[state] = cycle

    # print(f"{target=}\n{render(platform)}")

    return load(platform)


# noinspection DuplicatedCode
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    lines = pathlib.Path(args.f).read_text().splitlines()
    platform = [[rock for rock in line] for line in lines]

    print("part 1:", part1(copy.deepcopy(platform)))
    print("part 2:", part2(copy.deepcopy(platform), cycles=10**9))


if __name__ == "__main__":
    main()
