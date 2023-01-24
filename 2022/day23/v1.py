"""Day 23: Unstable Diffusion"""

import argparse
import pathlib
from copy import copy
from typing import NamedTuple


class Position(NamedTuple):
    r: int
    c: int

    def __repr__(self):
        return f"<{self.r}, {self.c}>"

    def __add__(self, other):
        return Position(self.r + other[0], self.c + other[1])


class Grove:
    def __init__(self, elves: set[Position]):
        self.elves = elves
        self.num_elves = len(elves)
        self.dir_order = ["N", "S", "W", "E"]

    def region(self) -> tuple[Position, Position]:
        min_r = min(e.r for e in self.elves)
        min_c = min(e.c for e in self.elves)
        max_r = max(e.r for e in self.elves)
        max_c = max(e.c for e in self.elves)
        return Position(min_r, min_c), Position(max_r, max_c)

    def area(self) -> int:
        nw_corner, se_corner = self.region()
        ns_len = se_corner.r - nw_corner.r + 1
        ew_len = se_corner.c - nw_corner.c + 1
        return ns_len * ew_len

    def empty_ground(self) -> int:
        return self.area() - len(self.elves)

    def propose_move(self, pos: Position) -> Position | None:
        N1 = dict(
            N=Position(-1, 0),
            S=Position(+1, 0),
            W=Position(0, -1),
            E=Position(0, +1),
        )
        N3 = dict(
            N=(Position(-1, c) for c in (-1, 0, 1)),
            S=(Position(+1, c) for c in (-1, 0, 1)),
            W=(Position(r, -1) for r in (-1, 0, 1)),
            E=(Position(r, +1) for r in (-1, 0, 1)),
        )
        valid_moves = []
        for d4 in self.dir_order:
            if self.elves.isdisjoint(pos + nbr for nbr in N3[d4]):
                valid_moves.append(pos + N1[d4])
        if 0 < len(valid_moves) < 4:
            return valid_moves[0]
        return None

    def update(self, moves) -> bool:
        assert self.elves == moves.keys(), moves
        next_elves = set(moves.values())
        if moved := next_elves != self.elves:
            self.elves = next_elves
        return moved

    def round(self) -> bool:
        proposals = {}
        for elf in self.elves:
            move = self.propose_move(elf)
            if move is None:
                proposals[elf] = [elf]
            elif move in proposals:
                proposals[move].append(elf)
            else:
                proposals[move] = [elf]

        moves = {}
        for move, elves in proposals.items():
            assert len(elves) > 0, (move, elves)
            if len(elves) == 1:
                for elf in elves:
                    moves[elf] = move
            else:
                for elf in elves:
                    moves[elf] = elf

        moved = self.update(moves)
        self.dir_order.append(self.dir_order.pop(0))

        return moved

    def render(self, header=""):
        img = []
        nw_corner, se_corner = self.region()
        for r in range(nw_corner.r, se_corner.r + 1):
            for c in range(nw_corner.c, se_corner.c + 1):
                img.append("#" if (r, c) in self.elves else ".")
            img.append("\n")
        print(header + "\n" + "".join(img))


def part1(grove: Grove, num_rounds: int, display: bool):
    if display:
        grove.render(header=f"round: {0}")

    for i in range(1, num_rounds + 1):
        moved = grove.round()
        if display:
            grove.render(header=f"round: {i}, {moved=}")

    return grove.empty_ground()


def part2(grove: Grove, display: bool):
    if display:
        grove.render(header=f"round: {0}")

    i = 1
    while moved := grove.round():
        if display:
            grove.render(header=f"round: {i}, {moved=}")
        i += 1

    if display:
        grove.render(header=f"round: {i}, {moved=}")

    return i


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    parser.add_argument("-d", action="store_true", help="display")
    args = parser.parse_args()

    lines = pathlib.Path(args.f).read_text().strip().split("\n")
    R = len(lines)
    C = len(lines[0])
    elves = set()
    for r in range(R):
        for c in range(C):
            if lines[r][c] == "#":
                elves.add(Position(r, c))

    grove1 = Grove(copy(elves))
    grove2 = Grove(elves)

    print("part 1:", part1(grove=grove1, num_rounds=10, display=args.d))
    print("part 2:", part2(grove=grove2, display=args.d))


if __name__ == "__main__":
    main()
