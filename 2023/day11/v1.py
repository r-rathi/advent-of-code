"""Day 11: Cosmic Expansion"""

import argparse
import itertools
import pathlib


def partx(image, expansion_ratio):
    R, C = len(image), len(image[0])

    empty_rows = [r for r, row in enumerate(image) if all(p == "." for p in row)]
    empty_cols = [c for c, col in enumerate(zip(*image)) if all(p == "." for p in col)]

    galaxies = []
    er, ec = 0, 0
    for r in range(R):
        for c in range(C):
            if image[r][c] == "#":
                galaxies.append((er, ec))
            ec += expansion_ratio if c in empty_cols else 1
        er += expansion_ratio if r in empty_rows else 1
        ec = 0

    pairs = itertools.combinations(galaxies, 2)
    distances = [abs(f[0] - g[0]) + abs(f[1] - g[1]) for f, g in pairs]

    return sum(distances)


# noinspection DuplicatedCode
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    lines = pathlib.Path(args.f).read_text().splitlines()
    image = [line for line in lines]

    print("part 1:", partx(image, expansion_ratio=2))
    print("part 2:", partx(image, expansion_ratio=int(1e6)))


if __name__ == "__main__":
    main()
