"""Day 18: Lavaduct Lagoon

    Tags: #polygon-area #pick's-theorem #shoelace-formula

    https://en.wikipedia.org/wiki/Pick%27s_theorem
    For a polygon with all vertices on integer grid, it's area is given by:
      A = I + B / 2 - 1, where I = interior points and B = boundary points

    https://en.wikipedia.org/wiki/Shoelace_formula
    For a polygon with vertices (x0, y0), (x1, y1), ..., (xn, yn), area is given by:
    A = 1/2 * (x0 * y1 - x1 * y0 + x1 * y2 - x2 * y1 + ... + xn * y0 - x0 * yn)

    In this problem we are given a dig plan, which we can use to find the integer
    coordinates (xi, yi) of the vertices as well as the number of boundary points B.
    We can then use the shoelace formula to find the area A of the polygon, and then
    use Pick's theorem to find the number of intertior points I. The final answer
    then is B + I = B + A - B / 2 + 1 = A + B / 2 + 1.

"""

import argparse
import pathlib
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Step(NamedTuple):
    dx: int
    dy: int


DIRECTIONS = "RDLU"
STEP = dict(R=Step(1, 0), D=Step(0, 1), L=Step(-1, 0), U=Step(0, -1))


def step(point: Point, direction: str, n: int = 1) -> Point:
    x, y = point
    dx, dy = STEP[direction]
    return Point(x + dx * n, y + dy * n)


def polygon(digplan: list[tuple[str, int]]) -> tuple[list[Point], int]:
    vertices = []
    B = 0

    p = Point(0, 0)
    for direction, meters in digplan:
        vertices.append(p)
        B += meters
        p = step(p, direction, meters)

    assert p == (0, 0), p

    return vertices, B


def shoelace(vertices: list[Point]) -> int:
    area = 0
    for i in range(len(vertices)):
        x0, y0 = vertices[i - 1]
        x1, y1 = vertices[i]
        area += x0 * y1 - x1 * y0
    return area // 2


def part1(lines):
    digplan = []
    for line in lines:
        direction, meters, _ = line.split()
        digplan.append((direction, (int(meters))))

    vertices, B = polygon(digplan)
    A = shoelace(vertices)

    return A + B // 2 + 1


def part2(lines):
    digplan = []
    for line in lines:
        _, _, other = line.split()
        meters = int(other[2:7], 16)
        direction = DIRECTIONS[int(other[7])]
        digplan.append((direction, meters))

    vertices, B = polygon(digplan)
    A = shoelace(vertices)

    return A + B // 2 + 1


# noinspection DuplicatedCode
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    parser.add_argument("-d", action="store_true", help="display")
    args = parser.parse_args()

    lines = pathlib.Path(args.f).read_text().splitlines()

    print("part 1:", part1(lines))
    print("part 2:", part2(lines))


if __name__ == "__main__":
    main()
