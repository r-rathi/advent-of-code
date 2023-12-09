"""Day 7: Camel Cards"""

import argparse
import pathlib
from collections import Counter

CARDS1 = "23456789TJQKA"
CARDS2 = "J23456789TQKA"


def strength(hand: str, use_joker: bool = False) -> int:
    counter = Counter(hand)
    jokers = counter["J"] if use_joker else 0
    counts = sorted(counter.values(), reverse=True)

    if len(counts) == 1 and counts == [5]:
        return 6

    if len(counts) == 2 and counts == [4, 1]:
        if jokers == 0:
            return 5
        else:
            return 6

    if len(counts) == 2 and counts == [3, 2]:
        if jokers == 0:
            return 4
        else:
            return 6

    if len(counts) == 3 and counts == [3, 1, 1]:
        if jokers == 0:
            return 3
        else:
            return 5

    if len(counts) == 3 and counts == [2, 2, 1]:
        if jokers == 0:
            return 2
        elif jokers == 1:
            return 4
        elif jokers == 2:
            return 5

    if len(counts) == 4 and counts == [2, 1, 1, 1]:
        if jokers == 0:
            return 1
        else:
            return 3

    if len(counts) == 5 and counts == [1, 1, 1, 1, 1]:
        if jokers == 0:
            return 0
        else:
            return 1

    raise ValueError(f"bad hand: {hand} (counts = {counts}")


def total_winnings(hand_bids: dict[str, int], use_joker=False):
    cards = CARDS2 if use_joker else CARDS1

    strengths = {}
    for hand, bid in hand_bids.items():
        s = strength(hand, use_joker)
        v = tuple(cards.index(card) for card in hand)
        strengths[(s, v)] = hand

    total = 0
    for rank, (s, v) in enumerate(sorted(strengths.keys()), start=1):
        hand = strengths[(s, v)]
        bid = hand_bids[hand]
        # print(rank, s, hand, bid)
        total += rank * bid

    return total


# noinspection DuplicatedCode
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    lines = pathlib.Path(args.f).read_text().splitlines()

    hand_bids = {}
    for line in lines:
        hand, bid = line.split()
        hand_bids[hand] = int(bid)

    print("part 1:", total_winnings(hand_bids, use_joker=False))
    print("part 2:", total_winnings(hand_bids, use_joker=True))


if __name__ == "__main__":
    main()
