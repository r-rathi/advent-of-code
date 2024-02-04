"""Day 24: Never Tell Me The Odds"""

import argparse
import pathlib
import re
from itertools import combinations
from typing import NamedTuple

import sympy
from sympy import symbols, Matrix


class V3(NamedTuple):
    x: int
    y: int
    z: int


class H(NamedTuple):
    p: V3
    v: V3

    def __call__(self, t: float) -> tuple[float, float, float]:
        x = self.p.x + self.v.x * t
        y = self.p.y + self.v.y * t
        z = self.p.z + self.v.z * t
        return x, y, z


def path_intersection_xy(g: H, h: H) -> tuple[float, float]:
    """
    Given two paths g(s) and h(t), we need to solve for s, t such that

        g(s) = g.p + g.v * s = h(t) = h.p + h.v * t
    =>
        g.v * s - h.v * t = h.p - g.p
    =>
        g.v.x * s - h.v.x * t = h.p.x - g.p.x
        g.v.y * s - h.v.y * t = h.p.y - g.p.y
    """
    A = [[g.v.x, -h.v.x], [g.v.y, -h.v.y]]
    b = [h.p.x - g.p.x, h.p.y - g.p.y]
    return solve(A, b)


def solve(A, b):
    """Solve the 2x2 system Ax = b"""
    D = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    return (
        ((b[0] * A[1][1] - b[1] * A[0][1]) / D),
        ((b[1] * A[0][0] - b[0] * A[1][0]) / D),
    )


def part1(hailstones, lo, hi):
    within = []
    for a, b in combinations(hailstones, 2):
        try:
            s, t = path_intersection_xy(a, b)
            x, y, z = a(s)
            if s > 0 and t > 0 and lo <= x <= hi and lo <= y <= hi:
                within.append(a)
        except ZeroDivisionError:
            pass

    return len(within)


def part2(hailstones):
    # Rock
    rps = symbols("rpx rpy rpz")
    rvs = symbols("rvx rvy rvz")
    t = symbols("t")
    rp = Matrix(rps)
    rv = Matrix(rvs)
    r = rp + rv * t

    # Pick 3 hailstones
    hs = [Matrix(h.p) + Matrix(h.v) * t for h in hailstones[:3]]

    # Solve for rp, rv, and collision times t0, t1, t2
    ts = symbols("t0 t1 t2")
    system = [(r - hs[i]).subs(t, ts[i]) for i in range(3)]
    solution = sympy.solve(system)

    # for eqs in system:
    #     for eq in eqs:
    #         sympy.pprint(eq, use_unicode=True)
    # print(solution)

    return sum(solution[0][rps[i]] for i in range(3))


# noinspection DuplicatedCode
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    if args.f == "input.txt":
        lo, hi = 2 * 10**14, 4 * 10**14
    else:
        lo, hi = 7, 27

    lines = pathlib.Path(args.f).read_text().splitlines()

    hailstones = []
    for line in lines:
        px, py, pz, vx, vy, vz = [int(n) for n in re.findall(r"-?\d+", line)]
        p = V3(px, py, pz)
        v = V3(vx, vy, vz)
        hailstones.append(H(p, v))

    print("part 1:", part1(hailstones, lo, hi))
    print("part 2:", part2(hailstones))


if __name__ == "__main__":
    main()
