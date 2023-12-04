"""Day 5: Hydrothermal Venture"""

import argparse
import pathlib
import re
from collections import Counter
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


def inc_range(m, n):
    if m <= n:
        return range(m, n + 1, 1)
    else:
        return range(m, n - 1, -1)


class Line(NamedTuple):
    p0: Point
    p1: Point

    @property
    def is_horizontal(self):
        return self.p0.y == self.p1.y

    @property
    def is_vertical(self):
        return self.p0.x == self.p1.x

    @property
    def is_diagonal(self):
        dx = self.p1.x - self.p0.x
        dy = self.p1.y - self.p0.y
        return abs(dx) == abs(dy)

    def horizontal_points(self):
        return [Point(x, self.p0.y) for x in inc_range(self.p0.x, self.p1.x)]

    def vertical_points(self):
        return [Point(self.p0.x, y) for y in inc_range(self.p0.y, self.p1.y)]

    def diagonal_points(self):
        xs = inc_range(self.p0.x, self.p1.x)
        ys = inc_range(self.p0.y, self.p1.y)
        return [Point(x, y) for x, y in zip(xs, ys)]


def part1(lines):
    vents = []
    for line in lines:
        if line.is_horizontal:
            vents.extend(line.horizontal_points())
        elif line.is_vertical:
            vents.extend(line.vertical_points())

    counts = Counter(vents)
    overlapping_points = [p for p, cnt in counts.items() if cnt >= 2]

    return len(overlapping_points)


def part2(lines):
    vents = []
    for line in lines:
        if line.is_horizontal:
            vents.extend(line.horizontal_points())
        elif line.is_vertical:
            vents.extend(line.vertical_points())
        elif line.is_diagonal:
            vents.extend(line.diagonal_points())

    counts = Counter(vents)
    overlapping_points = [p for p, cnt in counts.items() if cnt >= 2]

    return len(overlapping_points)


def main():
    # noinspection DuplicatedCode
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    text_lines = pathlib.Path(args.f).read_text().splitlines()
    lines = []
    for text_line in text_lines:
        x0, y0, x1, y1 = [int(n) for n in re.findall(r"\d+", text_line)]
        lines.append(Line(Point(x0, y0), Point(x1, y1)))

    print("part 1:", part1(lines))
    print("part 2:", part2(lines))


if __name__ == "__main__":
    main()
