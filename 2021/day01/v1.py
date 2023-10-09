"""Day 1: Sonar Sweep"""

import argparse
import pathlib


def part1(depths):
    increased = [d0 < d1 for (d0, d1) in zip(depths[:-1], depths[1:])]
    return sum(increased)


def part2(depths):
    sliding_sums = [sum(w) for w in zip(depths[:-1], depths[1:], depths[2:])]
    increased = [d0 < d1 for (d0, d1) in zip(sliding_sums[:-1], sliding_sums[1:])]
    return sum(increased)


def main():
    # noinspection DuplicatedCode
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    lines = pathlib.Path(args.f).read_text().splitlines()
    numbers = [int(line.strip()) for line in lines]

    print("part 1:", part1(numbers))
    print("part 2:", part2(numbers))


if __name__ == "__main__":
    main()
