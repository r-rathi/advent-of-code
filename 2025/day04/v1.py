"""Day 4: Printing Department"""

RNBRS = [(-1, 0), (1, 0)]
CNBRS = [(0, -1), (0, 1)]
DNBRS = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
ANBRS = RNBRS + CNBRS + DNBRS


def is_accessible(grid: set[tuple[int, int]], pos: tuple[int, int]) -> bool:
    r, c = pos
    return sum((r + dr, c + dc) in grid for dr, dc in ANBRS) < 4


def part1(grid):
    return sum(is_accessible(grid, pos) for pos in grid)


def part2(grid):
    grid = grid.copy()
    removed = 0
    accessible = {pos for pos in grid if is_accessible(grid, pos)}
    while accessible:
        grid -= accessible
        removed += len(accessible)
        accessible = {pos for pos in grid if is_accessible(grid, pos)}
    return removed


def main():
    # noinspection DuplicatedCode
    import argparse
    import pathlib

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    lines = pathlib.Path(args.f).read_text().splitlines()
    R, C = len(lines), len(lines[0])
    grid = {(r, c) for r in range(R) for c in range(C) if lines[r][c] == "@"}

    print("part 1:", part1(grid))
    print("part 2:", part2(grid))


if __name__ == "__main__":
    main()
