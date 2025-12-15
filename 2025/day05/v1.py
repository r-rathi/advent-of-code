"""Day 5: Cafeteria"""


def part1(ranges, ids):
    fresh = [i for i in ids if any(i in r for r in ranges)]
    # print(fresh)
    return len(fresh)


def part2(ranges):
    sorted_ranges = sorted(ranges, key=lambda r: r.start)  # sorted by range.start
    disjoint_ranges = []
    a = sorted_ranges[0]  # accumulator
    for b in sorted_ranges[1:]:
        if b.start <= a.stop:
            a = range(a.start, max(a.stop, b.stop))  # accumulate
        else:
            disjoint_ranges.append(a)
            a = b
    disjoint_ranges.append(a)
    return sum(len(r) for r in disjoint_ranges)


def main():
    # noinspection DuplicatedCode
    import argparse
    import pathlib

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    range_lines, id_lines = pathlib.Path(args.f).read_text().strip().split("\n\n")
    ranges = [r.split("-") for r in range_lines.splitlines()]
    ranges = [range(int(a), int(b) + 1) for a, b in ranges]
    ids = [int(i) for i in id_lines.splitlines()]
    # print(ranges)
    # print(ids)

    print("part 1:", part1(ranges, ids))
    print("part 2:", part2(ranges))


if __name__ == "__main__":
    main()
