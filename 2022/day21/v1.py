"""Day 21: Monkey Math"""

import argparse
import pathlib


class Monkey:
    def __init__(self, name: str, job: "Job"):
        self.name = name
        self.job = job

    def yell(self, env: dict[str, "Monkey"]) -> int:
        return self.job(env)

    def __repr__(self):
        return f"{self.name}({self.job})"


class Job:
    def __call__(self, env: dict[str, Monkey]) -> int:
        raise NotImplementedError


class Number(Job):
    def __init__(self, value: int):
        self.value = value

    def __call__(self, env: dict[str, Monkey]) -> int:
        return self.value

    def __repr__(self):
        return f"{self.value}"


class BinOp(Job):
    def __init__(self, x: str, y: str):
        self.x = x
        self.y = y

    def __call__(self, env: dict[str, Monkey]) -> int:
        raise NotImplementedError


class AddOp(BinOp):
    def __call__(self, env: dict[str, Monkey]) -> int:
        xm = env[self.x]
        ym = env[self.y]
        return xm.yell(env) + ym.yell(env)

    def __repr__(self):
        return f"{self.x} + {self.y}"


class SubOp(BinOp):
    def __call__(self, env: dict[str, Monkey]) -> int:
        xm = env[self.x]
        ym = env[self.y]
        return xm.yell(env) - ym.yell(env)

    def __repr__(self):
        return f"{self.x} - {self.y}"


class MulOp(BinOp):
    def __call__(self, env: dict[str, Monkey]) -> int:
        xm = env[self.x]
        ym = env[self.y]
        return xm.yell(env) * ym.yell(env)

    def __repr__(self):
        return f"{self.x} * {self.y}"


class DivOp(BinOp):
    def __call__(self, env: dict[str, Monkey]) -> int:
        xm = env[self.x]
        ym = env[self.y]
        return xm.yell(env) // ym.yell(env)

    def __repr__(self):
        return f"{self.x} // {self.y}"


def part1(monkeys: dict[str, Monkey]) -> int:
    root = monkeys["root"]
    return root.yell(monkeys)


def part2(monkeys: dict[str, Monkey]) -> int:
    root = monkeys["root"]
    assert isinstance(root.job, BinOp), type(root.job)
    root.job = SubOp(root.job.x, root.job.y)

    humn = monkeys["humn"]
    assert isinstance(humn.job, Number), type(humn.job)

    def f(x):
        humn.job.value = x
        return root.yell(monkeys)

    def df(x, h):
        return (f(x + h) - f(x - h)) / (2 * h)

    def find_root(x0):
        # fast initial estimate using Newton-Raphson method
        x = x0
        h = 1
        while f(x) != 0:
            # print("find_root: newton:", x, h, f(x), df(x, h))
            try:
                x -= f(x) / df(x, h)
            except ZeroDivisionError:
                h += 1
        # print("find_root: newton>", x, h, f(x), df(x, h))

        # refine using linear search
        z = int(x) - 2 * h
        while f(z) != 0:
            # print("find_root: linear:", z, h, f(z), df(z, h))
            z += 1
        # print("find_root: linear>", z, h, f(z), df(z, h))

        return z

    return find_root(0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    lines = pathlib.Path(args.f).read_text().splitlines()

    monkeys = {}
    for line in lines:
        name, expr = line.split(":")
        tokens = expr.split()
        if len(tokens) == 1:
            job = Number(int(tokens[0]))
        elif tokens[1] == "+":
            job = AddOp(tokens[0], tokens[2])
        elif tokens[1] == "-":
            job = SubOp(tokens[0], tokens[2])
        elif tokens[1] == "*":
            job = MulOp(tokens[0], tokens[2])
        elif tokens[1] == "/":
            job = DivOp(tokens[0], tokens[2])
        else:
            raise SyntaxError(line)
        monkeys[name] = Monkey(name, job)

    # print(monkeys)

    print("part 1:", part1(monkeys))
    print("part 2:", part2(monkeys))


if __name__ == "__main__":
    main()
