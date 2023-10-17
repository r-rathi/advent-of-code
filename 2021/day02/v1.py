"""Day 2: Dive!"""

import argparse
import pathlib


def part1(commands):
    h, d = 0, 0  # horizontal position, depth
    for direction, step in commands:
        if direction == "down":
            d += step
        elif direction == "up":
            d -= step
        else:
            h += step
    print(h, d)
    return h * d


def part2(commands):
    h, d, a = 0, 0, 0  # horizontal position, depth, aim
    for direction, step in commands:
        if direction == "down":
            a += step
        elif direction == "up":
            a -= step
        else:
            h += step
            d += a * step
    print(h, d, a)
    return h * d


def main():
    # noinspection DuplicatedCode
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    lines = pathlib.Path(args.f).read_text().splitlines()

    commands = []  # command = (direction, step)
    for line in lines:
        direction, step = line.split()
        commands.append((direction, (int(step))))

    print("part 1:", part1(commands))
    print("part 2:", part2(commands))


if __name__ == "__main__":
    main()
