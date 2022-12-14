"""Day 11: Monkey in the Middle"""
import math
import pathlib
import sys
from copy import deepcopy


class Monkey:
    def __init__(self):
        self.id = None
        self.items = []
        self.op = None
        self.test = None
        self.dst_t = None
        self.dst_f = None
        self.count = 0

    def __repr__(self):
        return f"Monkey({self.id}, {self.items}, {self.op}, {self.test}, {self.dst_t}, {self.dst_f})"

    def play(self, monkeys: list["Monkey"], div, mod):
        for item in self.items:
            new = self.eval(old=item)
            new = new // div
            new = new % mod
            if new % self.test == 0:
                monkeys[self.dst_t].items.append(new)
            else:
                monkeys[self.dst_f].items.append(new)

        self.count += len(self.items)
        self.items = []

    def eval(self, old):
        new = eval(self.op, dict(old=old))
        # print(f"eval: '{op}' with old={old} --> {new}")
        return new


def parse_input(lines):
    monkeys = []

    for line in lines:
        words = line.strip().split()
        # print(words)
        if not words:
            continue

        if words[0] == "Monkey":
            monkeys.append(Monkey())
            monkeys[-1].id = words[1][:-1]
        elif words[0] == "Starting":
            items = "".join(words[2:]).split(",")
            monkeys[-1].items = [int(item) for item in items]
        elif words[0] == "Operation:":
            monkeys[-1].op = " ".join(words[-3:])
        elif words[0] == "Test:":
            monkeys[-1].test = int(words[-1])
        elif words[0] == "If" and words[1] == "true:":
            monkeys[-1].dst_t = int(words[-1])
        elif words[0] == "If" and words[1] == "false:":
            monkeys[-1].dst_f = int(words[-1])
        else:
            raise SyntaxError(line)

    return monkeys


def monkey_business(monkeys: list["Monkey"], rounds: int, div: int, mod: int):
    # print("begin:", [m.count for m in monkeys])
    # for i, monkey in enumerate(monkeys):
    #     print(i, monkey.items)

    for r in range(1, rounds + 1):
        for monkey in monkeys:
            monkey.play(monkeys=monkeys, div=div, mod=mod)

        # if r in [1, 20] or r % 1000 == 0:
        #     print(f"round {r}:", [m.count for m in monkeys])
        #     for i, monkey in enumerate(monkeys):
        #         print(i, monkey.items)

    return math.prod(sorted(m.count for m in monkeys)[-2:])


def part1(monkeys):
    return monkey_business(monkeys, rounds=20, div=3, mod=1)


def part2(monkeys):
    # With div now set to 1, the numbers (new = op(old)) start growing. To keep
    # the indefinite growth in check, we rely on the following observations:
    # 1. ops are either + or *
    # 2. new + a is divisible by d iff (new - d) + a is divisible by d, or
    #   (new - 2*d) + a, ..., or (new - q*d) + a is divisible by d, etc.
    #   In other words, "reducing" new by any multiple of d does not change the
    #   divisibility by d.
    # 3. as items are thrown around, we are testing divisibility by divisors
    #    d0, d1, ..., dn. Therefore, new can be reduced by d0 * d1 * ... * dn
    #    without affecting the test for divisibility by any of d0, d1, ..., dn.
    # 4. similar argument applies to new * b.
    mod = math.prod(m.test for m in monkeys)
    return monkey_business(monkeys, rounds=10000, div=1, mod=mod)


def main():
    input_file = "input.txt" if len(sys.argv) == 1 else sys.argv[1]
    lines = pathlib.Path(input_file).read_text().splitlines()

    monkeys = parse_input(lines)
    # for monkey in monkeys:
    #     print(monkey)

    monkeys1 = monkeys
    monkeys2 = deepcopy(monkeys)

    print("part 1:", part1(monkeys1))
    print("part 2:", part2(monkeys2))


if __name__ == "__main__":
    main()
