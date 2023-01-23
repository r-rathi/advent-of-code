"""Day 22: Monkey Map"""

import argparse
import pathlib
import re
import time
from typing import NamedTuple


FACE = ">v<^"
STEP = [(0, +1), (+1, 0), (0, -1), (-1, 0)]
TURN = dict(R=1, L=-1)

# Hard-coding the cube-nets for now
FACES1 = {
    "U": (0, 2),
    "D": (2, 2),
    "N": (1, 0),
    "S": (1, 2),
    "E": (2, 3),
    "W": (1, 1),
}
EDGES1 = {
    ("U", ">"): ("E", "<"),
    ("U", "v"): ("S", "v"),
    ("U", "<"): ("W", "v"),
    ("U", "^"): ("N", "v"),
    ("D", ">"): ("E", ">"),
    ("D", "v"): ("N", "^"),
    ("D", "<"): ("W", "^"),
    ("D", "^"): ("S", "^"),
    ("N", ">"): ("W", ">"),
    ("N", "v"): ("D", "^"),
    ("N", "<"): ("E", "^"),
    ("N", "^"): ("U", "v"),
    ("S", ">"): ("E", "v"),
    ("S", "v"): ("D", "v"),
    ("S", "<"): ("W", "<"),
    ("S", "^"): ("U", "^"),
    ("E", ">"): ("U", "<"),
    ("E", "v"): ("N", ">"),
    ("E", "<"): ("D", "<"),
    ("E", "^"): ("S", "<"),
    ("W", ">"): ("S", ">"),
    ("W", "v"): ("D", ">"),
    ("W", "<"): ("N", "<"),
    ("W", "^"): ("U", ">"),
}


FACES2 = {
    "U": (0, 1),
    "D": (2, 1),
    "N": (3, 0),
    "S": (1, 1),
    "E": (0, 2),
    "W": (2, 0),
}
EDGES2 = {
    ("U", ">"): ("E", ">"),
    ("U", "v"): ("S", "v"),
    ("U", "<"): ("W", ">"),
    ("U", "^"): ("N", ">"),
    ("D", ">"): ("E", "<"),
    ("D", "v"): ("N", "<"),
    ("D", "<"): ("W", "<"),
    ("D", "^"): ("S", "^"),
    ("N", ">"): ("D", "^"),
    ("N", "v"): ("E", "v"),
    ("N", "<"): ("U", "v"),
    ("N", "^"): ("W", "^"),
    ("S", ">"): ("E", "^"),
    ("S", "v"): ("D", "v"),
    ("S", "<"): ("W", "v"),
    ("S", "^"): ("U", "^"),
    ("E", ">"): ("D", "<"),
    ("E", "v"): ("S", "<"),
    ("E", "<"): ("U", "<"),
    ("E", "^"): ("N", "^"),
    ("W", ">"): ("D", ">"),
    ("W", "v"): ("N", "v"),
    ("W", "<"): ("U", ">"),
    ("W", "^"): ("S", ">"),
}


class Position(NamedTuple):
    r: int  # row
    c: int  # col
    f: str  # facing

    def __str__(self):
        return f"({self.r}, {self.c}) {self.f}"

    def facing(self):
        return FACE.index(self.f)


def part1(grid, moves, display=False):
    row_bounds = bounds(grid, axis=0)
    col_bounds = bounds(grid, axis=1)

    r, c = 0, row_bounds[0][0]
    pos = r, c
    face = 0  # >
    if display:
        render(grid, pos, FACE[face], f"start pos: pos, facing: {FACE[face]}")

    for move in moves:
        if move in TURN:
            turn = TURN[move]
            face = (face + turn) % 4
            if display:
                render(
                    grid,
                    pos,
                    FACE[face],
                    f"turn: {move} pos: {pos}, facing: {FACE[face]}",
                )
            continue

        steps = int(move)
        dr, dc = STEP[face]
        for i in range(steps):
            r, c = pos
            next_r = r + dr
            next_c = c + dc
            if face == 0 and next_c > row_bounds[r][1]:
                next_c = row_bounds[r][0]
            elif face == 1 and next_r > col_bounds[c][1]:
                next_r = col_bounds[c][0]
            elif face == 2 and next_c < row_bounds[r][0]:
                next_c = row_bounds[r][1]
            elif face == 3 and next_r < col_bounds[c][0]:
                next_r = col_bounds[c][1]

            if grid[next_r][next_c] == "#":
                break
            pos = next_r, next_c

            if display:
                render(
                    grid,
                    pos,
                    FACE[face],
                    f"step: {i + 1} of {steps} pos: {pos}, facing: {FACE[face]}",
                )

    print(f"final pos: {pos}, facing: {FACE[face]}")
    r, c = pos
    return 1000 * (r + 1) + 4 * (c + 1) + face


def bounds(grid, axis=0):
    shape = len(grid), len(grid[0])
    if axis == 0:

        def g(i, j):
            return grid[i][j]

        n0, n1 = shape
    else:

        def g(i, j):
            return grid[j][i]

        n0, n1 = reversed(shape)
    bs = []
    for i0 in range(n0):
        b0, b1 = None, None
        for i1 in range(n1):
            if g(i0, i1) != " ":
                b0 = i1
                break
        for i1 in range(n1 - 1, -1, -1):
            if g(i0, i1) != " ":
                b1 = i1
                break
        assert b0 is not None
        assert b1 is not None
        assert b0 <= b1, (b0, b1)
        bs.append((b0, b1))
    return bs


def render(grid, pos, marker, header=""):
    CLEAR_SCREEN = "\033[2J"
    BG_GREEN = "\033[42m"
    RESET = "\033[0m"
    marker = BG_GREEN + marker + RESET

    R, C = len(grid), len(grid[0])
    DR = 80
    if R > DR:
        R0 = max(0, pos[0] - DR // 2)
        R1 = R0 + DR
        if R1 >= R:
            R1 = R
            R0 = R1 - DR
    else:
        R0, R1 = 0, R

    img = []
    for r in range(R0, R1):
        row = []
        for c in range(C):
            row.append(marker if (r, c) == pos else grid[r][c])
        img.append("".join(row))
    print(CLEAR_SCREEN + header + "\n" + "\n".join(img))
    time.sleep(0.05)


class CubeNet:
    def __init__(self, size, faces, edges, grid, pos: Position):
        self.size = size
        self.faces = faces
        self.names = {v: k for k, v in faces.items()}
        self.edges = edges
        self.grid = grid
        self.pos = pos

    def wrap(self, r, c, next_f):
        turn = (FACE.index(next_f) - FACE.index(self.pos.f)) % 4
        if turn == 0:
            return r, c
        if turn == 1:
            return c, self.size - 1 - r
        if turn == 2:
            return self.size - 1 - r, self.size - 1 - c
        if turn == 3:
            return self.size - 1 - c, r
        raise ValueError(f"bad turn: {turn}")

    def turn(self, t, display):
        next_f = FACE[(FACE.index(self.pos.f) + TURN[t]) % 4]
        self.pos = Position(self.pos.r, self.pos.c, next_f)
        if display:
            self.render(f"turn: {t} pos: {self.pos}")

    def next_pos(self) -> Position:
        tile = self.pos.r // self.size, self.pos.c // self.size
        name = self.names[tile]

        step_r, step_c = STEP[FACE.index(self.pos.f)]
        next_r = self.pos.r + step_r
        next_c = self.pos.c + step_c
        next_f = self.pos.f

        next_dr = next_r % self.size
        next_dc = next_c % self.size

        if (
            self.pos.f == ">"
            and next_dc == 0
            or self.pos.f == "v"
            and next_dr == 0
            or self.pos.f == "<"
            and next_dc == self.size - 1
            or self.pos.f == "^"
            and next_dr == self.size - 1
        ):
            next_name, next_f = self.edges[(name, self.pos.f)]
            next_tr, next_tc = self.faces[next_name]
            next_dr, next_dc = self.wrap(next_dr, next_dc, next_f)
            next_r, next_c = (
                next_tr * self.size + next_dr,
                next_tc * self.size + next_dc,
            )

        return Position(next_r, next_c, next_f)

    def step(self, steps, display):
        for i in range(steps):
            next_pos = self.next_pos()
            if self.grid[next_pos.r][next_pos.c] == "#":
                return
            self.pos = next_pos
            if display:
                self.render(f"step: {i + 1} of {steps} pos: {self.pos}")

    def render(self, header=""):
        CLEAR_SCREEN = "\033[2J"
        BG_GREEN = "\033[42m"
        RESET = "\033[0m"
        marker = BG_GREEN + self.pos.f + RESET

        R, C = len(self.grid), len(self.grid[0])
        DR = 80
        if R > DR:
            R0 = max(0, self.pos.r - DR // 2)
            R1 = R0 + DR
            if R1 >= R:
                R1 = R
                R0 = R1 - DR
        else:
            R0, R1 = 0, R

        img = []
        for r in range(R0, R1):
            row = []
            for c in range(C):
                row.append(marker if (r, c) == (self.pos.r, self.pos.c) else self.grid[r][c])
            img.append("".join(row))
        print(CLEAR_SCREEN + header + "\n" + "\n".join(img))
        time.sleep(0.05)


def part2(grid, moves, display=False):
    row_bounds = bounds(grid, axis=0)
    start_pos = Position(0, row_bounds[0][0], ">")

    if len(grid) == 12:
        net = CubeNet(size=4, faces=FACES1, edges=EDGES1, pos=start_pos, grid=grid)
    else:
        net = CubeNet(size=50, faces=FACES2, edges=EDGES2, pos=start_pos, grid=grid)

    if display:
        net.render(f"start pos: {net.pos}")

    for move in moves:
        if move in TURN:
            net.turn(move, display)
        else:
            net.step(int(move), display)

    print(f"final pos: {net.pos}")
    return 1000 * (net.pos.r + 1) + 4 * (net.pos.c + 1) + net.pos.facing()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    parser.add_argument("-d", action="store_true", help="display")
    args = parser.parse_args()

    board, path = pathlib.Path(args.f).read_text().split("\n\n")
    board = board.split("\n")
    num_cols = max(len(row) for row in board)
    grid = []
    for row in board:
        grid.append(row + " " * (num_cols - len(row)))
    # print("\n".join("".join(row) for row in grid))
    # print(path)
    moves = re.split(r"([RL])", path.strip())
    # print(moves)

    print("part 1:", part1(grid, moves, display=args.d))
    print("part 2:", part2(grid, moves, display=args.d))


if __name__ == "__main__":
    main()
