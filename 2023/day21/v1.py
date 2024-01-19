"""Day 21: Step Counter

    Tags: #breadth-first-search #bfs #bfs-layers

    In this problem we need to find the number of nodes reachable from a starting
    node in a given number of steps. This can be found as follows:

    Let T[d] be the set of total nodes reachable from source s in d steps, then:
        T[d] = T[d-2] U N[d], where
        N[d] = { v | dmin(s, v) = d }. Also,
        T[0] = N[0] and T[1] = N[1].

    This can be seen as follows. We start from s and do a layer-by-layer BFS traversal,
    visiting the layer N[d], which is the set of new nodes at a distance d from the s.
    Now, consider we are at distance d-1, and going to layer d. The reachable nodes
    at distance d will include stepping back to layer d-2 and the new nodes at distance d.

"""

import argparse
import pathlib


def bfs_layers(neighbors, s):
    previous_layer = set()
    # noinspection PySetFunctionToLiteral
    current_layer = set([s])
    while current_layer:
        yield current_layer
        next_layer = {
            v for u in current_layer for v in neighbors(u) if v not in previous_layer
        }
        previous_layer, current_layer = current_layer, next_layer


def part1(grid, steps=64):
    R, C = len(grid), len(grid[0])

    s = next((r, c) for r in range(R) for c in range(C) if grid[r][c] == "S")

    def neighbors(v):
        r, c = v
        for dr, dc in [(-1, 0), (+1, 0), (0, -1), (0, +1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] != "#":
                yield nr, nc

    N = {}
    for d, layer in enumerate(bfs_layers(neighbors, s)):
        N[d] = layer
        if d == steps:
            break

    new = [len(N[d]) if d in N else 0 for d in range(steps + 1)]
    tot = [sum(new[d::-2]) for d in range(len(new))]

    # for d in N:
    #     layer = N.get(d, set())
    #     print(d, new[d], tot[d], layer)

    return tot[steps]


def part2(grid, steps=26501365):
    R, C = len(grid), len(grid[0])

    s = next((r, c) for r in range(R) for c in range(C) if grid[r][c] == "S")

    # Infinitely repreating grid
    def neighbors(v):
        r, c = v
        for dr, dc in [(-1, 0), (+1, 0), (0, -1), (0, +1)]:
            nr, nc = r + dr, c + dc
            if grid[nr % R][nc % C] != "#":
                yield nr, nc

    # Given the open rows and columns in middle and on the edges of the grid, and
    # plenty of open diagonals in the outer "diamond", the layer pattern becomes
    # periodic (actually the delta_new) with period R (=C).

    new = {}
    for d, layer in enumerate(bfs_layers(neighbors, s)):
        new[d] = len(layer)
        if d == 3 * R - 1:
            break

    delta = [new[2 * R + d % R] - new[R + d % R] for d in range(R)]

    tot0, tot1 = new[0], new[1]
    for d in range(2, steps + 1):
        if d in new:
            tot0, tot1 = tot1, tot0 + new[d]
        else:
            tot0, tot1 = tot1, tot0 + new[R + d % R] + delta[d % R] * (d // R - 1)

    return tot1


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
