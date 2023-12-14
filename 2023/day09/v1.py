"""Day 9: Mirage Maintenance"""

import argparse
import pathlib


def diff(ns):
    return [n1 - n0 for n0, n1 in zip(ns[:-1], ns[1:])]


def extrapolate_forward(ns):
    if all(n == 0 for n in ns):
        return 0
    return ns[-1] + extrapolate_forward(diff(ns))


def extrapolate_backward(ns):
    if all(n == 0 for n in ns):
        return 0
    return ns[0] - extrapolate_backward(diff(ns))


def part1(histories):
    return sum(extrapolate_forward(h) for h in histories)


def part2(histories):
    return sum(extrapolate_backward(h) for h in histories)


# noinspection DuplicatedCode
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    lines = pathlib.Path(args.f).read_text().splitlines()
    histories = [[int(n) for n in line.split()] for line in lines]

    print("part 1:", part1(histories))
    print("part 2:", part2(histories))


if __name__ == "__main__":
    main()
