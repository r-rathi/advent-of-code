"""Day 19: Aplenty"""

import argparse
import pathlib
from collections import deque, defaultdict
from math import prod


def apply_rules(part, rules):
    for condition, next_workflow in rules[:-1]:
        if eval(condition, {}, part):
            return next_workflow
    return rules[-1][-1]


def part1(system, parts):
    accepted = []
    rejected = []
    for part in parts:
        workflow = "in"
        while workflow not in "AR":
            workflow = apply_rules(part, system[workflow])

        if workflow == "A":
            accepted.append(part)
        elif workflow == "R":
            rejected.append(part)

    return sum(sum(part.values()) for part in accepted)


class Interval:
    def __init__(self, name: str, lo: int, hi: int) -> None:
        assert lo <= hi, (lo, hi)
        self.name = name
        self.lo = lo
        self.hi = hi

    def __repr__(self):
        return f"{self.name}[{self.lo}, {self.hi})"

    def __lt__(self, other: int) -> tuple["Interval", "Interval"]:
        if other < self.lo:
            return Interval(self.name, 0, 0), self
        if self.hi <= other:
            return self, Interval(self.name, 0, 0)
        return Interval(self.name, self.lo, other), Interval(self.name, other, self.hi)

    def __gt__(self, other: int) -> tuple["Interval", "Interval"]:
        if other < self.lo:
            return self, Interval(self.name, 0, 0)
        if self.hi <= other:
            return Interval(self.name, 0, 0), self
        return Interval(self.name, other + 1, self.hi), Interval(
            self.name, self.lo, other + 1
        )


def part2(system):
    part = dict(
        x=Interval("x", 1, 4001),
        m=Interval("m", 1, 4001),
        a=Interval("a", 1, 4001),
        s=Interval("s", 1, 4001),
    )

    accepted = []
    rejected = []

    parts_workflows = deque()
    parts_workflows.append((part, "in"))

    while parts_workflows:
        part, workflow = parts_workflows.popleft()

        if workflow == "A":
            accepted.append(part)
            continue

        if workflow == "R":
            rejected.append(part)
            continue

        rules = system[workflow]
        for condition, next_workflow in rules[:-1]:
            intv_t, intv_f = eval(condition, {}, part)
            part_t = {**part, intv_t.name: intv_t}
            part_f = {**part, intv_f.name: intv_f}
            parts_workflows.append((part_t, next_workflow))
            part = part_f
        parts_workflows.append((part, rules[-1][-1]))

    return sum(prod(i.hi - i.lo for i in part.values()) for part in accepted)


# noinspection DuplicatedCode
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    chunks = pathlib.Path(args.f).read_text().split("\n\n")

    system = defaultdict(list)
    for line in chunks[0].splitlines():
        workflow, rules = line.split("{")
        for rule in rules[:-1].split(","):
            system[workflow].append(rule.split(":"))

    parts = []
    for line in chunks[1].splitlines():
        expr = "dict(" + line[1:-1] + ")"
        part = eval(expr, {})
        parts.append(part)

    print("part 1:", part1(system, parts))
    print("part 2:", part2(system))


if __name__ == "__main__":
    main()
