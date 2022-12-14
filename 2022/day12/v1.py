"""Day 12: Hill Climbing Algorithm"""
import pathlib
import sys
from copy import deepcopy
from time import sleep


def bfs_wavefronts(graph, node):
    wavefront = {node}
    wavefronts = [wavefront]
    visited = {node}
    # print(wavefront)
    while wavefront := advance_wavefront(graph, wavefront, visited):
        wavefronts.append(wavefront)
        visited.update(wavefront)
        # print(wavefront)
    return wavefronts


def advance_wavefront(graph, wavefront, visited):
    new_wavefront = set()
    for node in wavefront:
        for new_node in graph[node]:
            if new_node not in visited:
                new_wavefront.add(new_node)
    return new_wavefront


def display_wavefronts(grid, wavefronts, start, end):
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    RESET = "\033[0m"

    sr, sc = start
    er, ec = end

    print("Wavefronts:")
    for wfn in range(len(wavefronts)):
        img = deepcopy(grid)
        img[sr][sc] = img[sr][sc].upper()
        img[er][ec] = img[er][ec].upper()

        for i, wf in enumerate(wavefronts):
            for r, c in wf:
                if i < wfn:
                    img[r][c] = BG_RED + img[r][c] + RESET
                elif i == wfn:
                    img[r][c] = BG_GREEN + img[r][c] + RESET
        img = "\n".join("".join(row) for row in img)

        print("wavefront", wfn)
        print(img)
        sleep(0.05)


def neighbors(r, c, num_rows, num_cols):
    return [
        (r + dr, c + dc)
        for (dr, dc) in [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if 0 <= r + dr < num_rows and 0 <= c + dc < num_cols
    ]


def part1(grid, start, end):
    num_rows, num_cols = len(grid), len(grid[0])

    graph = {}
    for r in range(num_rows):
        for c in range(num_cols):
            graph[(r, c)] = [
                (nr, nc)
                for nr, nc in neighbors(r, c, num_rows, num_cols)
                if ord(grid[nr][nc]) - ord(grid[r][c]) <= 1
            ]

    wavefronts = bfs_wavefronts(graph, start)

    display_wavefronts(grid, wavefronts, start, end)

    distances = [d for d, wf in enumerate(wavefronts) if end in wf]
    # print(distances)
    return distances[0]


def part2(grid, start, end):
    num_rows, num_cols = len(grid), len(grid[0])

    graph = {}
    for r in range(num_rows):
        for c in range(num_cols):
            graph[(r, c)] = [
                (nr, nc)
                for nr, nc in neighbors(r, c, num_rows, num_cols)
                if ord(grid[nr][nc]) - ord(grid[r][c]) >= -1
            ]

    wavefronts = bfs_wavefronts(graph, end)

    display_wavefronts(grid, wavefronts, start, end)

    distances = [
        d for d, wf in enumerate(wavefronts) if "a" in {grid[r][c] for r, c in wf}
    ]
    # print(distances)
    return distances[0]


def parse_input(lines):
    grid = []
    start = None
    end = None
    for r, line in enumerate(lines):
        row = []
        for c, char in enumerate(list(line)):
            if char == "S":
                start = (r, c)
                row.append("a")
            elif char == "E":
                end = (r, c)
                row.append("z")
            else:
                row.append(char)
        grid.append(row)
    return grid, start, end


def main():
    input_file = "input.txt" if len(sys.argv) == 1 else sys.argv[1]
    lines = pathlib.Path(input_file).read_text().splitlines()

    grid, start, end = parse_input(lines)

    print("part 1:", part1(grid, start, end))
    print("part 2:", part2(grid, start, end))


if __name__ == "__main__":
    main()
