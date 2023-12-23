"""Day 16: The Floor Will Be Lava"""

import argparse
import pathlib
from collections import defaultdict
from typing import NamedTuple


class Vec(NamedTuple):
    r: int
    c: int

    def __add__(self, other):
        r, c = other
        return Vec(self.r + r, self.c + c)


Tile = Vec
Beam = Vec
Node = tuple[Tile, Beam]


# Beam directions
E = Beam(0, 1)
N = Beam(-1, 0)
W = Beam(0, -1)
S = Beam(1, 0)

BEAMS = {E: ">", N: "^", W: "<", S: "v"}


class DoDad:
    _dodads = {
        ".": {E: [E], N: [N], W: [W], S: [S]},
        "/": {E: [N], N: [E], W: [S], S: [W]},
        "\\": {E: [S], N: [W], W: [N], S: [E]},
        "|": {E: [N, S], N: [N], W: [N, S], S: [S]},
        "-": {E: [E], N: [E, W], W: [W, ], S: [E, W]},
    }

    def __init__(self, name: str):
        self.name = name
        self.do = self._dodads[name]

    def __str__(self):
        return self.name

    def __call__(self, beam: Beam) -> list[Beam]:
        return self.do[beam]


class Contraption:
    def __init__(self, grid: list[str]):
        self.R = len(grid)
        self.C = len(grid[0])
        self.dodads = {}
        for r in range(self.R):
            for c in range(self.C):
                self.dodads[Tile(r, c)] = DoDad(grid[r][c])

    def neighbors(self, node: Node) -> list[Node]:
        tile, beam = node
        nbrs = []
        for nbr_beam in self.dodads[tile](beam):
            nbr_tile = tile + nbr_beam
            if 0 <= nbr_tile.r < self.R and 0 <= nbr_tile.c < self.C:
                nbrs.append((nbr_tile, nbr_beam))
        return nbrs

    def dfs(self, start: Node):
        stack = [start]
        visited = set()
        while stack:
            node = stack.pop()
            if node in visited:
                continue
            yield node
            visited.add(node)
            stack.extend(self.neighbors(node))

    def energize(self, start: Node) -> int:
        energized = defaultdict(list)
        for tile, beam in self.dfs(start):
            energized[tile].append(beam)

        total = sum(bool(beams) for beams in energized.values())

        # print("Beams:")
        # self.show_beams(energized)
        # print("Energized:", total)
        # self.show_energized(energized)

        return total

    def show_beams(self, energized):
        img = []
        for r in range(self.R):
            row = []
            for c in range(self.C):
                tile = Tile(r, c)
                name = self.dodads[tile].name
                if name == "." and energized[tile]:
                    num = len(energized[tile])
                    name = f"{num}" if num > 1 else BEAMS[energized[tile][0]]
                row.append(name)
            img.append("".join(row))
        print("\n".join(img))

    def show_energized(self, energized):
        img = []
        for r in range(self.R):
            row = []
            for c in range(self.C):
                row.append("#" if energized[Tile(r, c)] else ".")
            img.append("".join(row))
        print("\n".join(img))


def part1(grid):
    return Contraption(grid).energize(start=(Tile(0, 0), E))


def part2(grid):
    R, C = len(grid), len(grid[0])
    contraption = Contraption(grid)

    configs = [(Tile(0, c), S) for c in range(C)]
    configs += [(Tile(R - 1, c), N) for c in range(C)]
    configs += [(Tile(r, 0), E) for r in range(R)]
    configs += [(Tile(r, C - 1), W) for r in range(R)]

    energized = [(contraption.energize(start), start) for start in configs]
    energized.sort()
    # print("Best config:", energized[-1][1], energized[-1][0])

    return energized[-1][0]


# noinspection DuplicatedCode
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    grid = pathlib.Path(args.f).read_text().splitlines()

    print("part 1:", part1(grid))
    print("part 2:", part2(grid))


if __name__ == "__main__":
    main()
