"""Day 3: Binary Diagnostic"""

import argparse
import pathlib
from collections import Counter


def part1(rows: list[str]):
    bit_counters = [Counter(column) for column in zip(*rows)]

    mc_bits = [c.most_common()[0][0] for c in bit_counters]
    lc_bits = [c.most_common()[-1][0] for c in bit_counters]

    gamma_rate = int("".join(mc_bits), 2)
    epsilon_rate = int("".join(lc_bits), 2)

    power_consumption = gamma_rate * epsilon_rate
    return power_consumption


def part2(rows: list[str]):
    mc_rows = filter_rows(rows, most_common_bit_or_1)
    lc_rows = filter_rows(rows, least_common_bit_or_0)

    assert len(mc_rows) == 1, mc_rows
    assert len(lc_rows) == 1, lc_rows

    o2_generator_rating = int(mc_rows[0], 2)
    co2_scrubber_rating = int(lc_rows[0], 2)

    life_support_rating = o2_generator_rating * co2_scrubber_rating
    return life_support_rating


def filter_rows(rows, f):
    f_rows = rows[:]
    for c in range(len(rows[0])):
        if len(f_rows) <= 1:
            break
        f_bit = f(list(zip(*f_rows))[c])
        f_rows = [row for row in f_rows if row[c] == f_bit]
    return f_rows


def most_common_bit_or_1(bits):
    counts = Counter(bits)
    if counts["1"] < counts["0"]:
        return "0"
    return "1"


def least_common_bit_or_0(bits):
    counts = Counter(bits)
    if counts["1"] < counts["0"]:
        return "1"
    return "0"


def main():
    # noinspection DuplicatedCode
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    lines = pathlib.Path(args.f).read_text().splitlines()

    print("part 1:", part1(lines))
    print("part 2:", part2(lines))


if __name__ == "__main__":
    main()
