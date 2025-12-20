"""Day 8: Playground"""
import math
from typing import NamedTuple


class JBox(NamedTuple):
    x: int
    y: int
    z: int


type Circuit = frozenset[JBox]


def squared_distance(j1: JBox, j2: JBox) -> int:
    x1, y1, z1 = j1
    x2, y2, z2 = j2
    return (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2


def part1(jboxes: list[JBox], pairs: list[tuple[JBox, JBox]], max_connections: int) -> int:
    circuits: set[Circuit] = {frozenset([jbox]) for jbox in jboxes}
    playground: dict[JBox, Circuit] = {jbox: ckt for ckt in circuits for jbox in ckt}

    for i, (jbox1, jbox2) in enumerate(pairs, start=1):
        if i > max_connections:
            break
        ckt1 = playground[jbox1]
        ckt2 = playground[jbox2]

        if ckt1 == ckt2:
            continue

        connected_ckt = ckt1 | ckt2
        circuits.remove(ckt1)
        circuits.remove(ckt2)
        circuits.add(connected_ckt)
        for jbox in connected_ckt:
            playground[jbox] = connected_ckt

    sorted_circuits = sorted(circuits, key=lambda ckt: len(ckt), reverse=True)
    return math.prod(len(c) for c in sorted_circuits[:3])


def part2(jboxes: list[JBox], pairs: list[tuple[JBox, JBox]]) -> int:
    circuits = [{jbox} for jbox in jboxes]

    for jbox1, jbox2 in pairs:
        ckt1 = next(c for c in circuits if jbox1 in c)
        ckt2 = next(c for c in circuits if jbox2 in c)

        if ckt1 == ckt2:
            continue

        circuits.remove(ckt1)
        ckt2 |= ckt1

        if len(circuits) == 1:
            return jbox1[0] * jbox2[0]

    return -1


def main():
    # noinspection DuplicatedCode
    import argparse
    import pathlib

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    max_connections = 1000 if args.f == "input.txt" else 10

    lines = pathlib.Path(args.f).read_text().splitlines()

    jboxes: list[JBox] = []
    for line in lines:
        x, y, z = [int(n) for n in line.split(",")]
        jboxes.append(JBox(x, y, z))

    pairs = [(jbox1, jbox2) for i1, jbox1 in enumerate(jboxes) for jbox2 in jboxes[i1 + 1:]]
    pairs.sort(key=lambda p: squared_distance(*p))

    print("part 1:", part1(jboxes, pairs, max_connections))
    print("part 2:", part2(jboxes, pairs))


if __name__ == "__main__":
    main()
