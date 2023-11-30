"""Day 4: Giant Squid"""

import argparse
import pathlib


class Board:
    def __init__(self, grid):
        self.grid = grid
        self.num_rows = len(grid)
        self.num_cols = len(grid[0])

        self._inv_grid = {}
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                self._inv_grid[self.grid[r][c]] = (r, c)

        self._marks = [[0] * self.num_cols for _ in range(self.num_rows)]
        self._row_counts = [0] * self.num_rows
        self._col_counts = [0] * self.num_cols

    def mark(self, number):
        if number in self._inv_grid:
            r, c = self._inv_grid[number]
            self._marks[r][c] = True
            self._row_counts[r] += 1
            self._col_counts[c] += 1

    def unmarked_sum(self):
        usum = 0
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if not self._marks[r][c]:
                    usum += self.grid[r][c]
        return usum

    def complete(self):
        row_complete = self.num_cols in self._row_counts
        col_complete = self.num_cols in self._col_counts
        return row_complete or col_complete

    def render(self):
        board = []
        for r in range(self.num_rows):
            row = []
            for c in range(self.num_cols):
                num_mark = f"{self.grid[r][c]:2d}"
                if self._marks[r][c]:
                    num_mark += "[*]"
                else:
                    num_mark += "[ ]"
                row.append(num_mark)
            board.append("  ".join(row))
        return "\n".join(board)


def play(draws, grids, display=False, verbose=False):
    boards = [Board(g) for g in grids]
    wins = []
    for number in draws:
        if not boards:
            break
        if display and verbose:
            print("-" * 33)
            print(f"{number}:")
        next_boards = []
        for board in boards:
            board.mark(number)
            if display and verbose:
                print(board.render(), end="")
            if board.complete():
                wins.append((number, board))
                if display and verbose:
                    print(" <-- win", end="")
                    if len(wins) == 1:
                        print(" (first)", end="")
                    elif len(wins) == len(grids):
                        print(" (last)", end="")
            else:
                next_boards.append(board)
            if display and verbose:
                print("\n")

        boards = next_boards

    first_number, first_board = wins[0]
    last_number, last_board = wins[-1]

    if display:
        print("First win:", first_number)
        print(first_board.render(), "\n")
        print("Last win:", last_number)
        print(last_board.render(), "\n")

    first_score = first_number * first_board.unmarked_sum()
    last_score = last_number * last_board.unmarked_sum()

    return first_score, last_score


def main():
    # noinspection DuplicatedCode
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    parser.add_argument("-d", action="store_true", help="display")
    parser.add_argument("-v", action="store_true", help="verbose")
    args = parser.parse_args()

    chunks = pathlib.Path(args.f).read_text().strip().split("\n\n")
    draws = [int(n) for n in chunks[0].split(",")]
    grids = []
    for chunk in chunks[1:]:
        grid = []
        for line in chunk.strip().splitlines():
            row = [int(n) for n in line.split()]
            grid.append(row)
        grids.append(grid)

    scores = play(draws, grids, display=args.d, verbose=args.v)

    print("part 1:", scores[0])
    print("part 2:", scores[1])


if __name__ == "__main__":
    main()
