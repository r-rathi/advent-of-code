"""Day 13: Distress Signal"""
import functools
import math
import pathlib
import sys


def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        return compare_ints(left, right)

    if isinstance(left, int):
        return compare_lists([left], right)

    if isinstance(right, int):
        return compare_lists(left, [right])

    return compare_lists(left, right)


def compare_ints(left, right):
    return left - right


def compare_lists(left, right):
    if len(left) != 0 and len(right) != 0:
        return compare(left[0], right[0]) or compare(left[1:], right[1:])
    return len(left) - len(right)


def part1(pairs):
    comparisons = [compare(left, right) for left, right in pairs]
    # print(comparisons)
    return sum(i + 1 for i, c in enumerate(comparisons) if c < 0)


def part2(packets, divider_packets):
    packets.extend(divider_packets)
    packets.sort(key=functools.cmp_to_key(compare))
    # print(packets)
    return math.prod(i + 1 for i, p in enumerate(packets) if p in divider_packets)


def main():
    input_file = "input.txt" if len(sys.argv) == 1 else sys.argv[1]
    input_text = pathlib.Path(input_file).read_text().strip()

    paras = input_text.split("\n\n")
    pairs = [para.split("\n") for para in paras]
    pairs = [[eval(e) for e in pair] for pair in pairs]
    print("part 1:", part1(pairs))

    packets = []
    for pair in pairs:
        packets.extend(pair)
    print("part 2:", part2(packets, divider_packets=[[2], [6]]))


if __name__ == "__main__":
    main()
