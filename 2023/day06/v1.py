"""Day 6: Wait For It"""

import argparse
import pathlib
from math import prod, sqrt, ceil, floor


def timed(f):
    import time

    def timed_f(*args, **kwargs):
        start_time = time.perf_counter()
        result = f(*args, **kwargs)
        stop_time = time.perf_counter()
        return result, stop_time - start_time

    return timed_f


def part1(lines):
    trecs = [int(n) for n in lines[0].split()[1:]]
    drecs = [int(n) for n in lines[1].split()[1:]]
    # print(trecs, drecs)

    num_wins = []
    for trec, drec in zip(trecs, drecs):
        ds = [th * (trec - th) for th in range(trec + 1)]
        num_wins.append(sum(d > drec for d in ds))

    return prod(num_wins)


@timed
def part2(lines):
    trec = int("".join(lines[0].split()[1:]))
    drec = int("".join(lines[1].split()[1:]))
    # print(trec, drec)

    ds = [th * (trec - th) for th in range(trec + 1)]
    num_wins = sum(d > drec for d in ds)

    return num_wins


@timed
def part2_faster(lines):
    trec = int("".join(lines[0].split()[1:]))
    drec = int("".join(lines[1].split()[1:]))
    # print(trec, drec)

    th_range = sqrt(trec**2 - 4 * drec)
    th_lo = trec / 2 - th_range / 2
    th_hi = trec / 2 + th_range / 2
    num_wins = floor(th_hi) - ceil(th_lo) + 1

    return num_wins


# noinspection DuplicatedCode
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    lines = pathlib.Path(args.f).read_text().splitlines()

    print("part 1:", part1(lines))

    result, run_time = part2(lines)
    print("part 2:", result, f"({run_time:0.3e} secs)")

    result, run_time = part2_faster(lines)
    print("part 2:", result, f"({run_time:0.3e} secs)")


if __name__ == "__main__":
    main()
