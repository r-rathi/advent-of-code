"""Day 3: Gear Ratios"""

import argparse
import pathlib
from math import prod


def parse_numbers(schematic, R, C):
    # print("lines:")
    # print("\n".join(lines))
    numbers = []
    for r in range(R):
        row = []
        number = []

        for c in range(C):
            char = schematic[r][c]
            if char.isdigit():
                number.append((r, c))
            elif number:
                row.append(tuple(number))
                number = []

        if number:
            row.append(tuple(number))

        numbers.append(row)

    # print("numbers:")
    # for row in numbers:
    #     print(row)
    return numbers


RNBRS = [(0, -1), (0, 1)]
CNBRS = [(-1, 0), (1, 0)]
DNBRS = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
ANBRS = RNBRS + CNBRS + DNBRS


def neighbors(r, c, num_rows, num_cols, rel_nbrs):
    return [
        (r + dr, c + dc)
        for (dr, dc) in rel_nbrs
        if 0 <= r + dr < num_rows and 0 <= c + dc < num_cols
    ]


def part1(schematic):
    R, C = len(schematic), len(schematic[0])

    numbers = parse_numbers(schematic, R, C)

    symbols = [
        (r, c)
        for r in range(R)
        for c in range(C)
        if not (schematic[r][c].isdigit() or schematic[r][c] == ".")
    ]

    part_numbers = []
    for s in symbols:
        nbr_numbers = set(
            number
            for n in neighbors(*s, R, C, ANBRS)
            for number in numbers[n[0]]
            if n in number
        )
        part_numbers.extend(
            int("".join(schematic[r][c] for r, c in n)) for n in nbr_numbers
        )
    # print("part_numbers:", part_numbers)

    return sum(part_numbers)


def part2(schematic):
    R, C = len(schematic), len(schematic[0])

    numbers = parse_numbers(schematic, R, C)

    stars = [(r, c) for r in range(R) for c in range(C) if schematic[r][c] == "*"]

    part_numbers = {}
    for s in stars:
        nbr_numbers = set(
            number
            for n in neighbors(*s, R, C, ANBRS)
            for number in numbers[n[0]]
            if n in number
        )
        if len(nbr_numbers) == 2:
            part_numbers[s] = [
                int("".join(schematic[r][c] for r, c in n)) for n in nbr_numbers
            ]
    # print("part_numbers:", part_numbers)

    gear_ratios = {g: prod(part_numbers[g]) for g in part_numbers}
    # print("gear ratios:", gear_ratios)

    return sum(gear_ratios.values())


# noinspection DuplicatedCode
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    lines = pathlib.Path(args.f).read_text().splitlines()

    print("part 1:", part1(lines))
    print("part 2:", part2(lines))


if __name__ == "__main__":
    main()
