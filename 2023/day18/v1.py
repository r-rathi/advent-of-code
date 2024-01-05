"""Day 18: Lavaduct Lagoon

    Tags: #breadth-first-search #bfs #flood-fill #perimeter #area
    Tags: #polygon-area #shoelace-formula #trapeziod-formula #green's-theorem

"""

import argparse
import pathlib
import time
from typing import NamedTuple


class Position(NamedTuple):
    r: int
    c: int


class Motion(NamedTuple):
    dr: int
    dc: int


DIRECTIONS = "RDLU"
MOTIONS = dict(R=Motion(0, 1), D=Motion(1, 0), L=Motion(0, -1), U=Motion(-1, 0))


def step(position: Position, direction: str, n: int = 1) -> Position:
    r, c = position
    dr, dc = MOTIONS[direction]
    return Position(r + dr * n, c + dc * n)


class Lagoon1:
    def __init__(self, digplan: list[tuple[str, int, int]]) -> None:
        self.boundary: dict[Position, int] = {}
        self.interior: set[Position] = set()

        position = Position(0, 0)
        for direction, meters, color in digplan:
            for _ in range(meters):
                self.boundary[position] = color
                position = step(position, direction)
        assert position == (0, 0), position

        min_r = min(r for r, c in self.boundary)
        max_r = max(r for r, c in self.boundary)
        min_c = min(c for r, c in self.boundary)
        max_c = max(c for r, c in self.boundary)

        # Create a bounding box one meter larger on all sides
        self.top_left = Position(min_r - 1, min_c - 1)
        self.bottom_right = Position(max_r + 1, max_c + 1)

    def volume(self) -> int:
        return len(self.boundary) + len(self.interior)

    def fill(self, display=False) -> None:
        whole = {
            Position(r, c)
            for r in range(self.top_left.r, self.bottom_right.r + 1)
            for c in range(self.top_left.c, self.bottom_right.c + 1)
        }
        filled = set(self.boundary.keys())
        front = {self.top_left}
        while front:
            if display:
                self.animate_fill(filled, front)
            next_front = {
                next_position
                for position in front
                for direction in DIRECTIONS
                if (next_position := step(position, direction)) in whole
                and next_position not in filled
            }
            filled.update(front)
            front = next_front
        self.interior = whole - filled

    def animate_fill(self, filled, front) -> None:
        CLEAR_SCREEN = "\033[2J"
        img = []
        for r in range(self.top_left.r, self.bottom_right.r + 1):
            row = []
            for c in range(self.top_left.c, self.bottom_right.c + 1):
                if (r, c) in self.boundary:
                    point = "#"
                elif (r, c) in filled:
                    point = "*"
                elif (r, c) in front:
                    point = "@"
                else:
                    point = "."
                row.append(point)
            img.append("".join(row))
        print(CLEAR_SCREEN + "\n".join(img))
        time.sleep(0.1)

    def display(self) -> None:
        lagoon = self.boundary.keys() | self.interior
        img = []
        for r in range(self.top_left.r, self.bottom_right.r + 1):
            row = []
            for c in range(self.top_left.c, self.bottom_right.c + 1):
                point = "#" if (r, c) in lagoon else "."
                if (r, c) in self.boundary:
                    point = "#"
                elif (r, c) in self.interior:
                    point = "#"
                row.append(point)
            img.append("".join(row))
        print("\n".join(img))


class Lagoon2:
    def __init__(self, digplan: list[tuple[str, int, int]]) -> None:
        self.boundary: list[Position] = []

        # Find which way the trench turns with the given digplan
        clockwise = "RDLU" * 2
        anticlockwise = clockwise[::-1]

        turns = 0
        for i in range(len(digplan)):
            prev_direction, _, _ = digplan[i - 1]
            direction, _, _ = digplan[i]

            if prev_direction + direction in clockwise:
                turns += 1
            elif prev_direction + direction in anticlockwise:
                turns -= 1
            else:
                raise ValueError(f"Invalid directions {prev_direction} -> {direction}")

        if turns == 4:
            convex, concave = clockwise, anticlockwise
        elif turns == -4:
            convex, concave = anticlockwise, clockwise
        else:
            raise ValueError(f"Invalid turns {turns}")

        # Create the outer boundary of the trench, adjusting the edge length according to convexity
        position = Position(0, 0)
        for i in range(len(digplan)):
            self.boundary.append(position)

            prev_direction, _, _ = digplan[i - 1]
            direction, length, _ = digplan[i]
            next_direction, _, _ = digplan[(i + 1) % len(digplan)]

            if prev_direction + direction + next_direction in convex:
                length += 1
            elif prev_direction + direction + next_direction in concave:
                length -= 1

            position = step(position, direction, length)

        assert position == (0, 0), position

    def volume_shoelace(self) -> int:
        # https://en.wikipedia.org/wiki/Shoelace_formula#Shoelace_formula
        area = 0
        for i in range(len(self.boundary)):
            r0, c0 = self.boundary[i - 1]
            r1, c1 = self.boundary[i]
            area += r1 * c0 - r0 * c1
        return area // 2

    def volume_trapezoid(self) -> int:
        # https://en.wikipedia.org/wiki/Shoelace_formula#Trapezoid_formula
        area = 0
        for i in range(len(self.boundary)):
            r0, c0 = self.boundary[i - 1]
            r1, c1 = self.boundary[i]
            area += (r0 + r1) * (c0 - c1)
        return area // 2


def part1(lines, display=False):
    digplan = []
    for line in lines:
        direction, meters, color = line.split()
        meters = int(meters)
        color = int(color[2:-1], 16)
        digplan.append((direction, meters, color))

    lagoon = Lagoon1(digplan)
    if display:
        lagoon.display()
    lagoon.fill(display=display)
    if display:
        lagoon.display()

    return lagoon.volume()


def part2(lines):
    digplan = []
    for line in lines:
        _, color, other = line.split()
        meters = int(other[2:7], 16)
        direction = DIRECTIONS[int(other[7])]
        color = int(color)
        digplan.append((direction, meters, color))

    lagoon = Lagoon2(digplan)
    vol_shoelace = lagoon.volume_shoelace()
    vol_trapeziod = lagoon.volume_trapezoid()
    assert vol_shoelace == vol_trapeziod, (vol_shoelace, vol_trapeziod)

    return vol_shoelace


# noinspection DuplicatedCode
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    parser.add_argument("-d", action="store_true", help="display")
    args = parser.parse_args()

    lines = pathlib.Path(args.f).read_text().splitlines()

    print("part 1:", part1(lines, display=args.d))
    print("part 2:", part2(lines))


if __name__ == "__main__":
    main()
