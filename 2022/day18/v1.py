"""Day 18: Boiling Boulders"""

import argparse
import pathlib
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int
    z: int


class Cube(NamedTuple):
    # Origin
    x: int
    y: int
    z: int

    def corners(self):
        return [
            Point(self.x + dx, self.y + dy, self.z + dz)
            for dx in (0, 1)
            for dy in (0, 1)
            for dz in (0, 1)
        ]

    def faces(self):
        return [
            tuple(p for p in self.corners() if p.x == self.x),
            tuple(p for p in self.corners() if p.x == self.x + 1),
            tuple(p for p in self.corners() if p.y == self.y),
            tuple(p for p in self.corners() if p.y == self.y + 1),
            tuple(p for p in self.corners() if p.z == self.z),
            tuple(p for p in self.corners() if p.z == self.z + 1),
        ]

    def x_neighbors(self):
        return [Cube(self.x + dx, self.y, self.z) for dx in (-1, 1)]

    def y_neighbors(self):
        return [Cube(self.x, self.y + dy, self.z) for dy in (-1, 1)]

    def z_neighbors(self):
        return [Cube(self.x, self.y, self.z + dz) for dz in (-1, 1)]

    def neighbors(self):
        return self.x_neighbors() + self.y_neighbors() + self.z_neighbors()


def surface(lava):
    s = set()
    for cube in lava:
        s.symmetric_difference_update(cube.faces())
    return s


def outer_surface(lava):
    # To find the outer surface area of lava, we bound the lava in a box 1 unit
    # larger on all sides. We then fill the box with water, starting from one
    # corner and identify all faces where water and lava make contact.
    xs = [c.x for c in lava]
    ys = [c.y for c in lava]
    zs = [c.z for c in lava]
    lo = Cube(min(xs) - 1, min(ys) - 1, min(zs) - 1)
    hi = Cube(max(xs) + 1, max(ys) + 1, max(zs) + 1)

    def in_box(c: Cube):
        return lo.x <= c.x <= hi.x and lo.y <= c.y <= hi.y and lo.z <= c.z <= hi.z

    boundary = {lo}
    filled = set()
    water_surface = set()
    while boundary:
        next_boundary = set()
        for water_cube in boundary:
            next_boundary.update(
                neighbor
                for neighbor in water_cube.neighbors()
                if in_box(neighbor)
                and neighbor not in filled
                and neighbor not in boundary
                and neighbor not in lava
            )
            water_surface.symmetric_difference_update(water_cube.faces())
        filled.update(boundary)
        boundary = next_boundary

    lava_surface = surface(lava)
    water_lava_interface = water_surface.intersection(lava_surface)
    return water_lava_interface


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    lines = pathlib.Path(args.f).read_text().splitlines()

    lava = set()
    for line in lines:
        x, y, z = [int(n) for n in line.split(",")]
        lava.add(Cube(x, y, z))

    surface_area = len(surface(lava))
    print("part 1:", surface_area)

    outer_surface_area = len(outer_surface(lava))
    print("part 2:", outer_surface_area)


if __name__ == "__main__":
    main()
