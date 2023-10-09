"""Day 25: Full of Hot Air"""

import argparse
import pathlib


def parse_snafu(string):
    m = {"-": -1, "=": -2}
    return [m.get(c) or int(c) for c in reversed(string)]


def format_snafu(s):
    m = {-1: "-", -2: "="}
    return "".join(m.get(d) or str(d) for d in reversed(s))


def from_snafu(s):
    n = 0
    b = 1
    for d in s:
        n += d * b
        b *= 5
    return n


def to_snafu(n):
    r = n
    s = []
    while r > 0:
        d = r % 5
        if d > 2:
            d = d - 5
        r = (r - d) // 5
        s.append(d)
    return s


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    lines = pathlib.Path(args.f).read_text().splitlines()

    snafus = [parse_snafu(line) for line in lines]
    total = sum(from_snafu(s) for s in snafus)
    print("print 1:", format_snafu(to_snafu(total)))


if __name__ == "__main__":
    main()
