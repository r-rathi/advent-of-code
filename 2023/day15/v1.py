"""Day 15: Lens Library"""

import argparse
import pathlib


def hash_algo(s: str) -> int:
    result = 0
    for c in s:
        result += ord(c)
        result *= 17
        result %= 256
    return result


def part1(init_seq: list[str]) -> int:
    return sum(hash_algo(s) for s in init_seq)


def show(boxes: list[dict[str, int]]):
    for i, box in enumerate(boxes):
        if box:
            print(f"Box {i}:", end="")
            for label, f in box.items():
                print(f" [{label} {f}]", end="")
            print()


def part2(init_seq: list[str]) -> int:
    # box: dict[label: str, f: int] works nicely here because dicts are ordered
    boxes: list[dict[str, int]] = [{} for _ in range(256)]

    for op in init_seq:
        if op.endswith("-"):
            label = op[:-1]
            box = boxes[hash_algo(label)]
            if label in box:
                del box[label]
        else:
            label, f = op.split("=")
            box = boxes[hash_algo(label)]
            box[label] = int(f)

        # print(f'After "{op}":')
        # show(boxes)
        # print()

    return sum(
        i * j * f
        for i, box in enumerate(boxes, start=1)
        for j, f in enumerate(box.values(), start=1)
    )


# noinspection DuplicatedCode
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    line = pathlib.Path(args.f).read_text().strip()
    init_seq = line.split(",")

    print("part 1:", part1(init_seq))
    print("part 2:", part2(init_seq))


if __name__ == "__main__":
    main()
