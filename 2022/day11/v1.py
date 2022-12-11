""""""
import sys
import pathlib


def eval_exp(op, old):
    new = eval(op, dict(old=old))
    # print(f"eval: '{op}' with old={old} --> {new}")
    return new


class Monkey:
    def __init__(self):  # , id, items, op, test, dst_t, dst_f):
        self.id = None
        self.items = []
        self.op = None
        self.test = None
        self.dst_t = None
        self.dst_f = None
        self.count = 0

    def __repr__(self):
        return f"Monkey({self.id}, {self.items}, {self.op}, {self.test}, {self.dst_t}, {self.dst_f})"

    def play(self, monkeys: list["Monkey"], worry_div=1):
        num_items = len(self.items)
        self.count += num_items
        for _ in range(num_items):
            item = self.items.pop(0)
            new = eval_exp(op=self.op, old=item)
            new = new // worry_div
            if new % self.test == 0:
                monkeys[self.dst_t].items.append(new)
            else:
                monkeys[self.dst_f].items.append(new)


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


def monkey_business(monkeys: list["Monkey"], num_rounds: int, worry_div: int):

    # for i, monkey in enumerate(monkeys):
    #     print(i, monkey.items)

    for r in range(1, num_rounds + 1):
        for monkey in monkeys:
            monkey.play(monkeys, worry_div)

        if r in [1, 20] or r % 100 == 0:
            print("round:", r, [m.count for m in monkeys])
            # for i, monkey in enumerate(monkeys):
            #     print(i, monkey.items)

    inspections = [m.count for m in monkeys]
    inspections.sort(reverse=True)
    return inspections[0] * inspections[1]


def part1(lines):
    monkeys = parse_input(lines)
    for monkey in monkeys:
        print(monkey)
    return monkey_business(monkeys, num_rounds=20, worry_div=3)


def part2(lines):
    monkeys = parse_input(lines)
    for monkey in monkeys:
        print(monkey)
    return monkey_business(monkeys, num_rounds=10000, worry_div=1)


def main():
    input_file = "input.txt" if len(sys.argv) == 1 else sys.argv[1]
    lines = pathlib.Path(input_file).read_text().splitlines()

    print("part 1:", part1(lines))
    print("part 2:", part2(lines))


if __name__ == "__main__":
    main()
