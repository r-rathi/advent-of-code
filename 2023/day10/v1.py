"""Day 10: Pipe Maze

    Tags: #breadth-first-search #bfs #perimeter #area
"""

import argparse
import pathlib

TILE_DNBRS = {
    "|": {(-1, 0), (1, 0)},
    "-": {(0, -1), (0, 1)},
    "L": {(-1, 0), (0, 1)},
    "J": {(0, -1), (-1, 0)},
    "7": {(0, -1), (1, 0)},
    "F": {(1, 0), (0, 1)},
}

TILE_3X = {
    ".": "..." "..." "...",
    "|": ".|." ".|." ".|.",
    "-": "..." "---" "...",
    "L": ".|." ".L-" "...",
    "J": ".|." "-J." "...",
    "7": "..." "-7." ".|.",
    "F": "..." ".F-" ".|.",
}


def make_graph(grid, R, C):
    S = None
    graph = {}
    for r in range(R):
        for c in range(C):
            tile = grid[r][c]
            if tile in TILE_DNBRS:
                graph[(r, c)] = {(r + dr, c + dc) for dr, dc in TILE_DNBRS[tile]}
            elif tile == "S":
                S = (r, c)

    if S is not None:
        S_nbrs = tuple(t for t in graph if S in graph[t])
        assert len(S_nbrs) == 2, S_nbrs
        graph[S] = set(S_nbrs)

    return graph, S


def find_loop(graph, S):
    nodes = {S}
    loop = set()
    step = -1
    while nodes:
        step += 1
        # print(step, nodes)
        next_nodes = set()
        for node in nodes:
            next_nodes.update(n for n in graph[node] if n in graph and n not in loop)
        loop.update(nodes)
        nodes = next_nodes
    assert len(loop) // 2 == step, (len(loop), step)
    return loop


def find_interior(boundary, grid, R, C):
    assert grid[0][0] == ".", grid[0][0]
    front = {(0, 0)}
    filled = set(boundary)
    step = -1
    while front:
        step += 1
        # print(step, front)
        next_front = set()
        for node in front:
            r, c = node
            for dr, dc in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                nbr = nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and nbr not in filled:
                    next_front.add(nbr)
        filled.update(front)
        front = next_front
    whole = set((r, c) for r in range(R) for c in range(C))
    return whole - filled


def part1(grid, R, C):
    graph, S = make_graph(grid, R, C)
    loop = find_loop(graph, S)
    return len(loop) // 2


def part2(grid, R, C):
    graph1x, S = make_graph(grid, R, C)
    S_dnbrs = {(nbr[0] - S[0], nbr[1] - S[1]) for nbr in graph1x[S]}
    S_tile = next((t for t, dnbrs in TILE_DNBRS.items() if dnbrs == S_dnbrs), None)
    # print("S:", S, graph1x[S], S_dnbrs, S_tile)
    # print("\n".join(grid))

    # Magnify the grid 3x by expanding each tile into a 3x3 tile
    grid3x = [[None] * 3 * C for _ in range(3 * R)]
    for r in range(R):
        for c in range(C):
            tile = S_tile if (r, c) == S else grid[r][c]
            for dr in range(3):
                for dc in range(3):
                    grid3x[3 * r + dr][3 * c + dc] = TILE_3X[tile][3 * dr + dc]
    # print("\n".join("".join(row) for row in grid3x))

    graph3x, _ = make_graph(grid3x, 3 * R, 3 * C)
    S3x = S[0] * 3 + 1, S[1] * 3 + 1
    boundary3x = find_loop(graph3x, S3x)
    interior3x = find_interior(boundary3x, grid3x, 3 * R, 3 * C)
    interior1x = {(r, c) for r, c in interior3x if r % 3 == 1 and c % 3 == 1}
    # print(interior1x)
    return len(interior1x)


# noinspection DuplicatedCode
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    grid = pathlib.Path(args.f).read_text().splitlines()
    R = len(grid)
    C = len(grid[0])

    print("part 1:", part1(grid, R, C))
    print("part 2:", part2(grid, R, C))


if __name__ == "__main__":
    main()
