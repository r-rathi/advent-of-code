"""Day 5: If You Give A Seed A Fertilizer"""

import argparse
import pathlib
from typing import NamedTuple


class Range(NamedTuple):
    a: int
    b: int

    def __repr__(self):
        return f"<{self.a}, {self.b}>"

    def __bool__(self):
        return self.a < self.b


def map_range(src: Range, ranges: list[tuple[Range, int]]) -> list[Range]:
    dst = []
    x = src
    for r, l in sorted(ranges):
        if not x:
            return dst

        if y := Range(x.a, min(x.b, r.a)):
            dst.append(y)

        if y := Range(max(x.a, r.a) + l, min(x.b, r.b) + l):
            dst.append(y)

        x = Range(max(x.a, r.b), x.b)

    if x:
        dst.append(x)

    return dst


def partx(maps, seeds, verbose=False):
    locations = []
    for seed in seeds:
        srcs = [seed]
        for name, ranges in maps.items():
            dsts = [dst for src in srcs for dst in map_range(src, ranges)]
            if verbose:
                print(f"* {name:24}:", srcs, "->", dsts)
            srcs = dsts
        if verbose:
            print()
        locations.extend(srcs)

    locations.sort()
    if verbose:
        print("locations:", locations)

    return locations[0].a


# noinspection DuplicatedCode
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    parser.add_argument("-v", action="store_true", help="verbose")
    args = parser.parse_args()

    seeds_line, *map_chunks = pathlib.Path(args.f).read_text().split("\n\n")
    seeds = [int(n) for n in seeds_line[6:].split()]
    # print(seeds)

    maps = {}
    for chunk in map_chunks:
        lines = chunk.splitlines()
        name = lines[0].split()[0]
        ranges = []
        for line in lines[1:]:
            dst_start, src_start, range_length = [int(n) for n in line.split()]
            ranges.append(
                (Range(src_start, src_start + range_length), dst_start - src_start)
            )
        maps[name] = sorted(ranges)

    # for m in maps:
    #     print(m)

    print("part 1:", partx(maps, [Range(s, s + 1) for s in seeds], verbose=args.v))
    print(
        "part 2:",
        partx(
            maps,
            [Range(s, s + l) for s, l in zip(seeds[::2], seeds[1::2])],
            verbose=args.v,
        ),
    )


if __name__ == "__main__":
    main()
