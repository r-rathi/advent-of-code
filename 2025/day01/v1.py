"""Day 1: Secret Entrance"""

import argparse
import pathlib


def part1(rotations, start):
    pointer = start
    password = 0
    for rotation in rotations:
        pointer = (pointer + rotation) % 100
        # print(rotation, pointer)
        if pointer == 0:
            password += 1
    return password


def part2(rotations, start):
    pointer = start
    password = 0

    for rotation in rotations:
        new_pointer = (pointer + rotation) % 100

        if rotation >= 0:
            # count (100 * n - 1) -> (100 * n) crossings
            crossings = (pointer + rotation) // 100
        else:
            # count (100 * n + 1) -> (100 * n) crossings
            crossings = ((-pointer) % 100 - rotation) // 100

        # print(f"{pointer:3d} {rotation:6d} -> {crossings:6d} {new_pointer:3d}")
        pointer = new_pointer
        password += crossings

    return password


def main():
    # noinspection DuplicatedCode
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    lines = pathlib.Path(args.f).read_text().splitlines()

    rotations = []
    for line in lines:
        direction = line[0]
        distance = int(line[1:])
        rotation = -distance if direction == "L" else distance
        rotations.append(rotation)
    # print(rotations)

    print("part 1:", part1(rotations, start=50))
    print("part 2:", part2(rotations, start=50))


if __name__ == "__main__":
    main()
