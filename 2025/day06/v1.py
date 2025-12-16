"""Day 6: Trash Compactor"""

from itertools import groupby
from math import prod

OPS = {"+": sum, "*": prod}


def part1(lines):
    ops = lines[-1].split()

    # Numbers read horizontally
    # 123 328  51 64
    #  45 64  387 23
    #   6 98  215 314
    # ->
    # [[123, 328, 51, 64], [45, 64, 387, 23], [6, 98, 215, 314]]
    rows = [[int(n) for n in line.split()] for line in lines[:-1]]

    # Transpose
    # [[123, 328, 51, 64], [45, 64, 387, 23], [6, 98, 215, 314]]
    # ->
    # [[123, 45, 6], [328, 64, 98], [51, 387, 215], [64, 23, 314]]
    cols = list(zip(*rows))

    return sum(OPS[op](col) for op, col in zip(ops, cols))


def part2(lines):
    ops = lines[-1].split()

    # Numbers read vertically by first transposing the text
    # 123 328  51 64
    #  45 64  387 23
    #   6 98  215 314
    # ->
    # ['1', '24', '356', '', '369', '248', '8', '', '32', '581', '175', '', '623', '431', '4']
    vlines = ["".join(vline).strip() for vline in zip(*lines[:-1])]

    # Split at ''
    # ['1', '24', '356', '', '369', '248', '8', '', '32', '581', '175', '', '623', '431', '4']
    # ->
    # [[1, 24, 356], [369, 248, 8], [32, 581, 175], [623, 431, 4]]
    cols = [[int(n) for n in group] for key, group in groupby(vlines, key=bool) if key]

    return sum(OPS[op](col) for op, col in zip(ops, cols))


def main():
    # noinspection DuplicatedCode
    import argparse
    import pathlib

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    lines = pathlib.Path(args.f).read_text().splitlines()

    print("part 1:", part1(lines))
    print("part 2:", part2(lines))


if __name__ == "__main__":
    main()
