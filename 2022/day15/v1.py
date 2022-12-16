"""Day 15: Beacon Exclusion Zone"""
import pathlib
import re
import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Interval(NamedTuple):
    # [left, right)
    left: int
    right: int

    def __str__(self):
        return f"[{self.left}, {self.right})"


def manhattan_distance(p0: Point, p1: Point):
    return abs(p0.x - p1.x) + abs(p0.y - p1.y)


def part1(sb_pairs, row_y):
    points = set()
    for s, b in sb_pairs:
        d = manhattan_distance(s, b)
        dy = abs(row_y - s.y)
        dx = d - dy
        if dx >= 0:
            points.update(range(s.x - dx, s.x + dx + 1))
        if b.y == row_y:
            points.remove(b.x)

    return len(points)


def part2(sb_pairs, bound):
    # for each y:
    # - find the x-interval that is within the radius of each sensor
    # - find the union of the intervals by attempting to merge the intervals
    # - if the merge fails because of non-overlap, that is out beacon
    sensor_radius = [(s, manhattan_distance(s, b)) for s, b in sb_pairs]
    beacon = None
    for y in range(bound + 1):
        x_intervals = []
        for s, r in sensor_radius:
            dy = abs(y - s.y)
            dx = r - dy
            if dx >= 0:
                x_intervals.append(Interval(s.x - dx, s.x + dx + 1))

        x_intervals.sort(key=lambda i: i.left)

        merged_interval = x_intervals[0]
        for interval in x_intervals[1:]:
            if merged_interval.right < interval.left:
                beacon = Point(merged_interval.right, y)
                break
            merged_interval = Interval(
                merged_interval.left, max(merged_interval.right, interval.right)
            )

        if beacon is not None:
            break

    assert beacon is not None
    # print("distress beacon:", beacon)
    return beacon.x * 4000000 + beacon.y


RE_INT = re.compile(r"[+-]?\d+")


def findall_ints(string: str) -> list:
    return [int(n) for n in RE_INT.findall(string)]


def main():
    if len(sys.argv) == 1:
        input_file = "input.txt"
        row_number = 2000000
        bound = 4000000
    elif len(sys.argv) == 2:
        input_file = sys.argv[1]
        row_number = 10
        bound = 20
    else:
        input_file = sys.argv[1]
        row_number = int(sys.argv[2])
        bound = int(sys.argv[3])

    lines = pathlib.Path(input_file).read_text().splitlines()

    sb_pairs = []
    for line in lines:
        sx, sy, bx, by = findall_ints(line)
        s = Point(sx, sy)
        b = Point(bx, by)
        sb_pairs.append((s, b))

    print("part 1:", part1(sb_pairs, row_y=row_number))
    print("part 2:", part2(sb_pairs, bound=bound))


if __name__ == "__main__":
    main()
