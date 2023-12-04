"""Day 4: Scratchcards"""

import argparse
import pathlib


def part1(cards):
    return sum(2 ** (n - 1) if n else 0 for n in cards)


def part2(cards):
    N = len(cards)
    count = [1] * N
    for i in range(N):
        js = list(range(i + 1, min(i + 1 + cards[i], N)))
        for j in js:
            count[j] += count[i]
    return sum(count)


# noinspection DuplicatedCode
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    lines = pathlib.Path(args.f).read_text().splitlines()
    cards = []
    for line in lines:
        c, ns = line.split(":")
        wns, hns = ns.split("|")
        wns = set(int(n) for n in wns.split())
        hns = set(int(n) for n in hns.split())
        cards.append(len(wns & hns))

    print("part 1:", part1(cards))
    print("part 2:", part2(cards))


if __name__ == "__main__":
    main()
