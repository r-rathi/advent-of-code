"""Day 9: Movie Theater

While part 1 was straightforward, part 2 ended up taking quite a bit of effort.

The first break through was realizing that we can reduce the problem from the
original fine tile grid to the much coarser non-uniform grid formed by the red
tiles (vertices of the polygon and the rectangle). Turns out this is a known
technique called *coordinate compression*.

The next step was to mark the interior points (on the coarse grid) of the
polygon. I had decided to use the ray casting approach to count boundary crossings,
but kept getting tripped up by the parallel edges. So, the second breakthough
was the realization that *concave corners must be deleted* as they are purely
internal turns and don't count as crossings.

 Convex corner A        Concave corner B
                               .......
   --> AXXXX               --> ...BXXX
       X....                   ...X
       X....                   ...X
       X....                   ...X

With these two ideas I was able to solve the problem. I then asked Claude for
a code review and after some back and forth hit upon another idea. I was using
set inclusion of boundary points for checking whether the rectangle fits in the
polygon and Claude suggested the *prefix-sum* approach along the rectangle
boundaries. I knew what prefix-sum was, but never realized this cool use of
prefix-sum for interval inclusion test! I wondered if we could extend this to a
2D variant and turns out this is an existing technique called *summed-area table*
or *integral image*.

Phew! This was hard, but also learned a lot.

References:
- https://stackoverflow.com/questions/29528934/coordinate-compression
- https://en.wikipedia.org/wiki/Point_in_polygon
- https://en.wikipedia.org/wiki/Summed-area_table
- https://en.wikipedia.org/wiki/Prefix_sum

Tags: #coordinate-compressions
Tags: #orientation #clockwise #anti-clockwise #convex #concave
Tags: #ray-casting
Tags: #prefix-sum #summed-area-table #integral-image
Tags: #llm
"""

type Point = tuple[int, int]
type Grid = list[list[bool]]


def orientation(polygon: list[Point]) -> int:
    """Return polygon winding direction using signed area.

    NB: uses the shoelace formula.
    For right-hand thumb rule +1 means counter-clockwise
    For left-hand thumb rule  +1 means clockwise.

    Returns: +1 (CW), -1 (CCW), or 0 (degenerate/collinear)
    """
    signed_area = sum(
        x1 * y2 - x2 * y1
        for (x1, y1), (x2, y2) in zip(polygon, polygon[1:] + polygon[:1])
    )
    return (signed_area > 0) - (signed_area < 0)


def compressed_grid(
    polygon: list[Point],
) -> tuple[Grid, dict[int, int], dict[int, int]]:
    """Build occupancy grid over compressed coordinates

    Returns: (grid, xindex, yindex)
    """
    # Coordinate compression
    xs, ys = zip(*polygon)
    xcoords = sorted(set(xs))
    ycoords = sorted(set(ys))
    xindex = {x: i for i, x in enumerate(xcoords)}
    yindex = {y: i for i, y in enumerate(ycoords)}

    polygon_orientation = orientation(polygon)
    nx, ny = len(xindex), len(yindex)

    # Occupancy grid: interior and boundary points marked as True
    grid: Grid = [[False] * nx for _ in range(ny)]
    n = len(polygon)

    # Mark points along horizontal edges as boundaries for vertical ray-casting
    for i in range(n):
        prev_pt, curr_pt, next_pt = polygon[i - 1], polygon[i], polygon[(i + 1) % n]
        x1, y1 = curr_pt
        x2, y2 = next_pt

        if y1 == y2:
            yi = yindex[y1]
            for xi in range(
                min(xindex[x1], xindex[x2]), max(xindex[x1], xindex[x2]) + 1
            ):
                grid[yi][xi] = True

        # Clear concave vertices because they are internal turns that don't count as crossings
        # NB: curr vertex is concave if  prev->curr->next triangle is opposite orientation from polygon
        if orientation([prev_pt, curr_pt, next_pt]) != polygon_orientation:
            grid[yindex[y1]][xindex[x1]] = False

    # Scan each column with inside/outside state toggle at each boundary
    for xi in range(nx):
        inside = False
        for yi in range(ny):
            on_boundary = grid[yi][xi]
            grid[yi][xi] = inside or on_boundary
            if on_boundary:
                inside = not inside

    return grid, xindex, yindex


def summed_area_table(grid: Grid) -> list[list[int]]:
    """2D summed-area table (padded to allow -1 indexing)

    This is like calculating F(x) = Integ(0..x) f(x)

    sat[y][x] = count of True cells in grid[:y+1, :x+1] = 2D cumulative sum

    a b => A B
    c d    C D

    B = A + b, C = a + C,
    D = A + b + c + d = d + (A + b) + (A + c) - A = d + B + C - A
    """
    ny, nx = len(grid), len(grid[0])
    sat = [
        [0] * (nx + 1) for _ in range(ny + 1)
    ]  # Padding to eliminate bound check for xi, yi = 0

    for yi in range(ny):
        for xi in range(nx):
            sat[yi][xi] = (
                grid[yi][xi] + sat[yi][xi - 1] + sat[yi - 1][xi] - sat[yi - 1][xi - 1]
            )

    return sat


def rect_sum(sat: list[list[int]], xi1: int, yi1: int, xi2: int, yi2: int) -> int:
    """Sum of values in rectangle (xi1,yi1) to (xi2,yi2) using padded SAT.

    This is like calculating Integ(x1..x2) f(x) = F(x2) - F(x1)

    A B => a b
    C D    c d

    b = B - A, c = C - A,
    d = D - b - c - A = D - (B - A) - (C - A) - A = D - B - C + A
    """
    return sat[yi2][xi2] - sat[yi2][xi1 - 1] - sat[yi1 - 1][xi2] + sat[yi1 - 1][xi1 - 1]


def rectangle_fits(
    sat: list[list[int]], xi1: int, yi1: int, xi2: int, yi2: int
) -> bool:
    """Check if rectangle is fully inside the polygon.

    If sum of interior cells == rectangle area, then ALL cells are inside.
    Uses SAT for O(1) instead of checking O(perimeter) boundary points.
    """
    if xi1 > xi2:
        xi1, xi2 = xi2, xi1
    if yi1 > yi2:
        yi1, yi2 = yi2, yi1
    expected = (xi2 - xi1 + 1) * (yi2 - yi1 + 1)
    return rect_sum(sat, xi1, yi1, xi2, yi2) == expected


def rectangle_area(p1: Point, p2: Point) -> int:
    """Calculate area of rectangle with opposite corners p1 and p2."""
    x1, y1 = p1
    x2, y2 = p2
    return (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)


def part1(points: list[Point]) -> int:
    """Part 1: Largest rectangle from ANY two vertices."""
    return max(
        rectangle_area(points[i], points[j])
        for i in range(len(points) - 1)
        for j in range(i + 1, len(points))
    )


def part2(points: list[Point]) -> int:
    """Part 2: Largest rectangle that fits INSIDE the polygon."""
    grid, xindex, yindex = compressed_grid(points)
    sat = summed_area_table(grid)

    return max(
        rectangle_area(points[i], points[j])
        for i in range(len(points) - 1)
        for j in range(i + 1, len(points))
        if rectangle_fits(
            sat,
            xindex[points[i][0]],
            yindex[points[i][1]],
            xindex[points[j][0]],
            yindex[points[j][1]],
        )
    )


def main():
    import argparse
    import pathlib

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    lines = pathlib.Path(args.f).read_text().splitlines()
    red_tiles: list[Point] = []
    for line in lines:
        x, y = map(int, line.split(","))
        red_tiles.append((x, y))

    print("part 1:", part1(red_tiles))
    print("part 2:", part2(red_tiles))


if __name__ == "__main__":
    main()
