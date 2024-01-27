"""Day 23: A Long Walk

    Tags: #longest-path #dfs
"""

import argparse
import pathlib
import sys

sys.setrecursionlimit(10000)

DIRS = {">": (0, +1), "v": (+1, 0), "<": (0, -1), "^": (-1, 0)}


def find_longest_path_length(graph, s, t):
    paths = 0
    longest = 0

    def dfs(u, path, length):
        nonlocal paths
        nonlocal longest

        if u == t:
            paths += 1
            if length > longest:
                longest = length
                # print("path:", paths, length, longest)
            return

        path.add(u)
        for v, d in graph[u].items():
            if v not in path:
                dfs(v, path, length + d)
        path.remove(u)

    dfs(s, set(), 0)

    return longest


def part1(grid):
    R, C = len(grid), len(grid[0])

    s = 0, grid[0].index(".")
    t = R - 1, grid[R - 1].index(".")

    graph = {}
    for r in range(R):
        for c in range(C):
            if grid[r][c] != "#":
                graph[(r, c)] = {}
                if grid[r][c] in DIRS:
                    dr, dc = DIRS[grid[r][c]]
                    nr, nc = r + dr, c + dc
                    graph[(r, c)][(nr, nc)] = 1
                else:
                    for arrow, (dr, dc) in DIRS.items():
                        nr, nc = r + dr, c + dc
                        if nr in range(R) and nc in range(C) and grid[nr][nc] in [".", arrow]:
                            graph[(r, c)][(nr, nc)] = 1

    return find_longest_path_length(graph, s, t)


def collapse_linear_paths(graph):
    # A huge part of the graph is just linear paths (... u=v=w ... )
    # Collapsing linear paths into single edges reduces the size of the graph drastically!

    # for u in graph:
    #     print(u, graph[u])
    # print("|V| =", len(graph))

    linear_nodes = [v for v in graph if len(graph[v]) == 2]

    while linear_nodes:
        v = linear_nodes.pop()
        u, w = graph[v].keys()
        d_uv = graph[u].pop(v)
        d_wv = graph[w].pop(v)
        d_uw = d_uv + d_wv
        graph[u][w] = d_uw
        graph[w][u] = d_uw
        del graph[v]

    # for u in graph:
    #     print(u, graph[u])
    # print("|V| =", len(graph))


def part2(grid):
    R, C = len(grid), len(grid[0])

    s = 0, grid[0].index(".")
    t = R - 1, grid[R - 1].index(".")

    graph = {}
    for r in range(R):
        for c in range(C):
            if grid[r][c] != "#":
                graph[(r, c)] = {}
                for dr, dc in DIRS.values():
                    nr, nc = r + dr, c + dc
                    if nr in range(R) and nc in range(C) and grid[nr][nc] != "#":
                        graph[(r, c)][(nr, nc)] = 1

    collapse_linear_paths(graph)

    return find_longest_path_length(graph, s, t)


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
