"""Day 8: Treetop Tree House"""
import pathlib


def array1d(size, fill_value=None):
    return [fill_value] * size


def array2d(num_rows, num_cols, fill_value=None):
    return [array1d(num_cols, fill_value) for _ in range(num_rows)]


def print_array2d(a, name=""):
    if name:
        print(f"{name}:")
    for row in a:
        print(row)


def visibility(h):
    num_rows = len(h)
    num_cols = len(h[0])

    v = array2d(num_rows, num_cols, 0)

    for r in range(num_rows):
        max_h = -1
        max_c = 0
        for c in range(0, num_cols):
            if h[r][c] > max_h:
                max_h = h[r][c]
                max_c = c
                v[r][c] = 1
        max_h = -1
        for c in range(num_cols - 1, max_c, -1):
            if h[r][c] > max_h:
                max_h = h[r][c]
                v[r][c] = 1

    for c in range(num_cols):
        max_h = -1
        max_r = 0
        for r in range(0, num_rows):
            if h[r][c] > max_h:
                max_h = h[r][c]
                max_r = r
                v[r][c] = 1
        max_h = -1
        for r in range(num_rows - 1, max_r, -1):
            if h[r][c] > max_h:
                max_h = h[r][c]
                v[r][c] = 1

    return v


def scenic_score(h):
    num_rows = len(h)
    num_cols = len(h[0])

    left_edge = array2d(num_rows, num_cols, 0)
    right_edge = array2d(num_rows, num_cols, num_cols - 1)
    top_edge = array2d(num_rows, num_cols, 0)
    bottom_edge = array2d(num_rows, num_cols, num_rows - 1)
    score = array2d(num_rows, num_cols, 0)

    for r in range(num_rows):
        for c in range(1, num_cols):
            e = c - 1
            while e > 0 and h[r][e] < h[r][c]:
                e = left_edge[r][e]
            left_edge[r][c] = e

    for r in range(num_rows):
        for c in range(num_cols - 2, -1, -1):
            e = c + 1
            while e < num_cols - 1 and h[r][e] < h[r][c]:
                e = right_edge[r][e]
            right_edge[r][c] = e

    for c in range(num_cols):
        for r in range(1, num_rows):
            e = r - 1
            while e > 0 and h[e][c] < h[r][c]:
                e = top_edge[e][c]
            top_edge[r][c] = e

    for c in range(num_cols):
        for r in range(num_rows - 2, -1, -1):
            e = r + 1
            while e < num_rows - 1 and h[e][c] < h[r][c]:
                e = bottom_edge[e][c]
            bottom_edge[r][c] = e

    # print_array2d(left_edge, "left_edge")
    # print_array2d(right_edge, "right_edge")
    # print_array2d(top_edge, "top_edge")
    # print_array2d(bottom_edge, "bottom_edge")

    for r in range(num_rows):
        for c in range(num_cols):
            s = c - left_edge[r][c]
            s *= right_edge[r][c] - c
            s *= r - top_edge[r][c]
            s *= bottom_edge[r][c] - r
            score[r][c] = s

    return score


inp = pathlib.Path("input.txt").read_text().splitlines()

height_grid = [[int(e) for e in list(row)] for row in inp]
visibility_grid = visibility(height_grid)

num_visible = 0
for row in visibility_grid:
    num_visible += sum(row)
    # print("".join([str(v) for v in row]))

print("part 1:", num_visible)

score_grid = scenic_score(height_grid)
max_score = max(max(row) for row in score_grid)

print("part 2:", max_score)
