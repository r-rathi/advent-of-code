"""Day 2: Gift Shop"""

import argparse
import pathlib


def is_invalid_id1(i: int) -> bool:
    """ID which is just repeated digits is invalid, e.g. 55, 6464, 123123"""
    s: str = str(i)
    m = len(s) // 2
    return s[:m] == s[m:]


def part1(id_ranges):
    invalid_ids = [i for r in id_ranges for i in r if is_invalid_id1(i)]
    # print(invalid_ids)
    return sum(invalid_ids)


def has_repeats(s: str, n: int) -> bool:
    """Returns True if s has repeats of length n"""
    # assert 0 < n <= len(s)
    if n > len(s) // 2 or len(s) % n != 0:
        return False
    for i in range(n, len(s), n):
        if s[i : i + n] != s[:n]:
            return False
    return True


def is_invalid_id2(i: int) -> bool:
    """ID with some sequence of digits repeated at least twice is invalid.
    Examples:
        12341234 (1234 two times), 123123123 (123 three times),
        1212121212 (12 five times), and 1111111 (1 seven times) are all invalid.
    """
    s: str = str(i)
    for n in range(1, len(s) // 2 + 1):
        if has_repeats(s, n):
            return True
    return False


def part2(id_ranges):
    invalid_ids = [i for r in id_ranges for i in r if is_invalid_id2(i)]
    # print(invalid_ids)
    return sum(invalid_ids)


def main():
    # noinspection DuplicatedCode
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    id_ranges = pathlib.Path(args.f).read_text().replace("\n", "").split(",")
    id_ranges = [r.split("-") for r in id_ranges]
    id_ranges = [(range(int(a), int(b) + 1)) for a, b in id_ranges]
    # print(id_ranges)

    print("part 1:", part1(id_ranges))
    print("part 2:", part2(id_ranges))


if __name__ == "__main__":
    main()
