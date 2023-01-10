"""Day 20: Grove Positioning System"""

import argparse
import pathlib


def decrypt(ns, key=1, times=1):
    ns = [n * key for n in ns]
    ms = mix(ns, times=times)
    i0 = ms.index(0)
    cs = [ms[(i0 + di) % len(ms)] for di in (1000, 2000, 3000)]
    return sum(cs)


def mix(ns, times=1):
    ts = list(enumerate(ns))
    for _ in range(times):
        for t in enumerate(ns):
            i = ts.index(t)
            n = ts[i][1]
            j = (i + n) % (len(ts) - 1)
            ts.insert(j, ts.pop(i))
    return [t[1] for t in ts]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    lines = pathlib.Path(args.f).read_text().splitlines()
    numbers = [int(line.strip()) for line in lines]

    print("part 1:", decrypt(numbers))
    print("part 2:", decrypt(numbers, key=811589153, times=10))


if __name__ == "__main__":
    main()
