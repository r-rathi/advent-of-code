"""Day 13: Point of Incidence"""

import argparse
import pathlib


TBL = str.maketrans({".": "0", "#": "1"})


def find_mirror(pattern: list[str], smudges: int) -> int:
    # Converting pattern to numbers, e.g. "#.#" -> 0b101, allows a quick count
    # of positions that differ, a.k.a hamming-distance
    numbers = [int(p.translate(TBL), 2) for p in pattern]

    for i in range(1, len(numbers)):
        # split between (i-1, i), reflect, and count mismatches
        fwd = numbers[i:]
        rev = reversed(numbers[:i])
        dist = sum((f ^ r).bit_count() for f, r in zip(fwd, rev))
        if dist == smudges:
            return i

    return 0


def partx(patterns, smudges=0):
    total = 0
    for pattern in patterns:
        # row wise
        nr = find_mirror(pattern, smudges)

        # column wise
        pattern_t = ["".join(r) for r in zip(*pattern)]
        nc = find_mirror(pattern_t, smudges)

        total += 100 * nr + nc

    return total


# noinspection DuplicatedCode
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    chunks = pathlib.Path(args.f).read_text().split("\n\n")
    patterns = [chunk.splitlines() for chunk in chunks]

    print("part 1:", partx(patterns, smudges=0))
    print("part 2:", partx(patterns, smudges=1))


if __name__ == "__main__":
    main()
