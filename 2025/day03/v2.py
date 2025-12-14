"""Day 3: Lobby

This turns out to be a classic greedy algorithm optimally solved using a
monotonic stack with a drop budget.

Tags: #monotonic-stack
Tags: #llm
"""


def max_k_digit_subsequence(digits: list[int], k: int) -> list[int]:
    """
    Return the lexicographically maximum length-k subsequence of `digits`.

    Select exactly k digits while preserving left-to-right order.
    Greedy solution uses a monotonic decreasing stack and a drop budget.

    Time:  O(n)
    Space: O(n) worst-case auxiliary (O(k) returned)
    """
    n = len(digits)
    if not (0 <= k <= n):
        raise ValueError("k must be between 0 and len(digits)")
    if k == 0:
        return []

    drop = n - k
    stack: list[int] = []

    for d in digits:
        while drop and stack and stack[-1] < d:
            stack.pop()
            drop -= 1
        stack.append(d)

    return stack[:k]


def max_joltage(bank: list[int], batteries_on: int) -> int:
    digits = max_k_digit_subsequence(bank, batteries_on)
    # print(bank, digits)
    number = 0
    for d in digits:
        number = number * 10 + d
    return number


def main():
    # noinspection DuplicatedCode
    import argparse
    import pathlib

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    lines = pathlib.Path(args.f).read_text().splitlines()
    banks = [[int(d) for d in line] for line in lines]
    # print(banks)

    print("part 1:", sum(max_joltage(bank, batteries_on=2) for bank in banks))
    print("part 2:", sum(max_joltage(bank, batteries_on=12) for bank in banks))


if __name__ == "__main__":
    main()
