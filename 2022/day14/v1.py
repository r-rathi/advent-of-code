"""Day 14: Regolith Reservoir"""
import pathlib
import sys
from copy import deepcopy
from time import sleep
from typing import NamedTuple, Optional


class Point(NamedTuple):
    x: int
    y: int


class Cave:
    def __init__(self, hole: Point):
        self.rock = set()
        self.sand = set()
        self.hole = hole
        self.floor_y: Optional[int] = None
        self.bounds = (hole, hole)

    def add_rock(self, point: Point):
        self.rock.add(point)

    def add_sand(self, point: Point):
        self.sand.add(point)

    def add_floor(self, dy: int):
        self.floor_y = self.bounds[1].y + dy

    def update_bounds(self):
        min_x = min(self.rock, key=lambda p: p.x).x
        max_x = max(self.rock, key=lambda p: p.x).x
        min_y = min(self.rock, key=lambda p: p.y).y
        max_y = max(self.rock, key=lambda p: p.y).y
        assert min_x <= self.hole.x <= max_x
        assert self.hole.y <= min_y <= max_y
        min_y = self.hole.y
        self.bounds = Point(min_x, min_y), Point(max_x, max_y)

    def inside(self, pos: Point) -> bool:
        min_x, min_y = self.bounds[0]
        max_x, max_y = self.bounds[1]
        if self.floor_y is not None:
            return min_y <= pos.y <= self.floor_y
        return min_x <= pos.x <= max_x and min_y <= pos.y <= max_y

    def blocked(self, pos: Point) -> bool:
        return (
            pos in self.rock
            or pos in self.sand
            or (self.floor_y is not None and pos.y == self.floor_y)
        )

    def next_pos(self, pos: Point) -> Point | None:
        for dx, dy in [(0, 1), (-1, 1), (1, 1)]:
            p = Point(pos.x + dx, pos.y + dy)
            if not self.blocked(p):
                return p
        return None

    def resting_pos(self, pos: Point) -> Point | None:
        while True:
            next_pos = self.next_pos(pos)
            if next_pos is None:
                return pos
            if not self.inside(next_pos):
                return None
            pos = next_pos

    def render(self) -> str:
        self.update_bounds()
        min_x, min_y = self.bounds[0]
        max_x, max_y = self.bounds[1]
        img = []
        for y in range(min_y, max_y + 1):
            row = []
            for x in range(min_x, max_x + 1):
                if (x, y) in self.rock:
                    row.append("#")
                elif (x, y) in self.sand:
                    row.append("o")
                elif (x, y) == self.hole:
                    row.append("+")
                elif self.floor_y is not None and y == self.floor_y:
                    row.append("=")
                else:
                    row.append(".")
            img.append("".join(row))
        return "\n".join(img)


def part1(cave: Cave, render=False):
    while resting_pos := cave.resting_pos(cave.hole):
        cave.add_sand(resting_pos)
        if render:
            print(len(cave.sand))
            print(cave.render())
            sleep(0.02)

    return len(cave.sand)


def part2(cave: Cave, render=False):
    while resting_pos := cave.resting_pos(cave.hole):
        cave.add_sand(resting_pos)
        if render:
            print(len(cave.sand), resting_pos)
            print(cave.render())
            sleep(0.02)
        if resting_pos == cave.hole:
            break

    return len(cave.sand)


def main():
    input_file = "input.txt" if len(sys.argv) == 1 else sys.argv[1]
    lines = pathlib.Path(input_file).read_text().splitlines()
    paths = [line.split(" -> ") for line in lines]

    cave = Cave(hole=Point(500, 0))
    for path in paths:
        points = []
        for x_y in path:
            x, y = [int(n) for n in x_y.split(",")]
            points.append((x, y))

        for src, dst in zip(points[:-1], points[1:]):
            src_x, src_y = src
            dst_x, dst_y = dst
            if src_x == dst_x:
                x = src_x
                if dst_y < src_y:
                    src_y, dst_y = dst_y, src_y
                for y in range(src_y, dst_y + 1):
                    cave.add_rock(Point(x, y))
            else:
                y = src_y
                if dst_x < src_x:
                    src_x, dst_x = dst_x, src_x
                for x in range(src_x, dst_x + 1):
                    cave.add_rock(Point(x, y))
    cave.update_bounds()
    # print(cave.render())

    cave1 = deepcopy(cave)
    cave2 = cave
    cave2.add_floor(dy=2)

    print("part 1:", part1(cave1, render=False))
    print("part 2:", part2(cave2, render=False))


if __name__ == "__main__":
    main()
