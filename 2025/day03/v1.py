"""Day 3: Lobby"""

import argparse
import pathlib


def argmax(array):
    return max(range(len(array)), key=array.__getitem__)


def max_joltage(bank: list[int], battries_on: int) -> int:
    digits = []
    batteries = bank[:]
    for n in range(battries_on - 1, 0, -1):
        i = argmax(batteries[:-n])
        digits.append(batteries[i])
        batteries = batteries[i + 1:]
    digits.append(max(batteries))
    # print(bank, digits)
    return sum(d * 10 ** i for i, d in enumerate(reversed(digits)))


def main():
    # noinspection DuplicatedCode
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    lines = pathlib.Path(args.f).read_text().splitlines()
    banks = [[int(d) for d in line] for line in lines]
    # print(banks)

    print("part 1:", sum(max_joltage(bank, battries_on=2) for bank in banks))
    print("part 2:", sum(max_joltage(bank, battries_on=12) for bank in banks))


if __name__ == "__main__":
    main()
