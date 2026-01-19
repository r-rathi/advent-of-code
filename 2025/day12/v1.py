"""Day 12: Christmas Tree Farm

This puzzle was a classic case of "solve the actual problem in front of you"!

This is a polyomino packing problem, and is NP-complete in general. The example
input had me implementing backtracking search, but the actual input turned out
to be solvable with simple bounds checking alone:

- Upper bound: If total_area >= total_bbox_area, shapes fit trivially.
- Lower bound: If total_area < total_cells, shapes can't fit.

References:
- https://en.wikipedia.org/wiki/Polyomino

Tags: #polyomino #packing #bounds
"""

from typing import NamedTuple


class Shape(NamedTuple):
    bbox: int
    cells: int


class Region(NamedTuple):
    width: int
    length: int
    counts: tuple[int, ...]

    def __str__(self) -> str:
        dims = f"{self.width}x{self.length}"
        counts = " ".join(map(str, self.counts))
        return f"{dims:>5}: {counts}"

    @property
    def area(self) -> int:
        return self.width * self.length


def can_fit(
    shapes: list[Shape], counts: tuple[int, ...], available_area: int
) -> tuple[bool | None, int, int]:
    """
    Determine if shapes with given counts can fit in available area.

    Returns:
        (result, total_bbox, total_cells) where result is:
        - True: Shapes definitely fit (bounding boxes fit without overlap).
        - False: Shapes definitely don't fit (not enough cells).
        - None: Ambiguous (would require backtracking to determine).
    """
    total_bbox = sum(s.bbox * c for s, c in zip(shapes, counts))
    total_cells = sum(s.cells * c for s, c in zip(shapes, counts))

    if available_area >= total_bbox:
        return True, total_bbox, total_cells
    if available_area < total_cells:
        return False, total_bbox, total_cells
    return None, total_bbox, total_cells


def part1(shapes: list[Shape], regions: list[Region]) -> int:
    fits_count = 0
    ambiguous_count = 0

    for region in regions:
        result, total_bbox, total_cells = can_fit(shapes, region.counts, region.area)
        if result:
            fits_count += 1
        elif result is None:
            ambiguous_count += 1
            print(
                f"{region} is ambiguous "
                f"(cells={total_cells} <= area={region.area} < bbox={total_bbox})"
            )

    if ambiguous_count > 0:
        print(f"Warning: {ambiguous_count} regions need backtracking (not implemented)")

    return fits_count


def main() -> None:
    import argparse
    import pathlib

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    chunks = pathlib.Path(args.f).read_text().split("\n\n")

    shapes: list[Shape] = []
    for chunk in chunks[:-1]:
        _, *rows = chunk.splitlines()
        bbox = len(rows) * len(rows[0])
        cells = sum(row.count("#") for row in rows)
        shapes.append(Shape(bbox=bbox, cells=cells))

    regions: list[Region] = []
    for line in chunks[-1].splitlines():
        dims, *qtys = line.replace(":", "").split()
        width, length = map(int, dims.split("x"))
        counts = tuple(map(int, qtys))
        assert len(counts) == len(shapes), (len(counts), len(shapes))
        regions.append(Region(width=width, length=length, counts=counts))

    print("part 1:", part1(shapes, regions))


if __name__ == "__main__":
    main()
