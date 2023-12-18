"""Day 12: Hot Springs"""

import argparse
import pathlib
from functools import cache


@cache
def arrangements(groups: tuple[int], conditions: str) -> int:
    if not groups:
        if "#" in conditions:
            return 0
        return 1

    first, rest = groups[0], groups[1:]
    span = len(conditions) - sum(rest) - len(rest)

    n = 0
    for i in range(span - first):
        if "#" in conditions[:i]:
            break
        if "." in conditions[i: i + first]:
            continue
        if conditions[i + first] == "#":
            continue
        n += arrangements(rest, conditions[i + first + 1:])

    return n


def partx(records, copies=1):
    total_arrangements = 0
    for conditions, groups in records:
        conditions = "?".join(cs for cs in [conditions] * copies)
        conditions += "."  # padding to help with boundary condition
        groups = groups * copies
        n = arrangements(groups, conditions)
        total_arrangements += n
        # print(conditions[:-1], groups, "->", n)

    return total_arrangements


# noinspection DuplicatedCode
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    lines = pathlib.Path(args.f).read_text().splitlines()

    records = []
    for line in lines:
        conditions, groups = line.split()
        groups = tuple(int(n) for n in groups.split(","))
        records.append((conditions, groups))

    print("part 1:", partx(records, copies=1))
    print("part 2:", partx(records, copies=5))


if __name__ == "__main__":
    main()
