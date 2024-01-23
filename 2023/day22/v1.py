"""Day 22: Sand Slabs"""

import argparse
import itertools
import pathlib
import re
from collections import deque, defaultdict, Counter


class Brick:
    _count = itertools.count()

    def __init__(self, x1, y1, z1, x2, y2, z2):
        self.id = next(self._count)
        self.xr = range(x1, x2 + 1) if x1 <= x2 else range(x2, x1 + 1)
        self.yr = range(y1, y2 + 1) if y1 <= y2 else range(y2, y1 + 1)
        self.zr = range(z1, z2 + 1) if z1 <= z2 else range(z2, z1 + 1)
        self.xy = {(x, y) for x in self.xr for y in self.yr}

    def __hash__(self):
        return self.id

    def __repr__(self):
        return f"Brick({self.id}, {self.xr}, {self.yr}, {self.zr})"

    def drop(self):
        self.zr = range(self.zr.start - 1, self.zr.stop - 1)

    def is_over_ground(self):
        return self.zr.start == 1

    def is_over(self, other):
        if self.zr.start != other.zr.stop:
            return False
        return bool(self.xy & other.xy)


class Stack:
    def __init__(self, bricks):
        self.bricks = sorted(bricks, key=lambda b: b.zr.start)
        self.above = {}  # above[brick] = bricks supported by this brick
        self.below = {}  # below[brick] = bricks supporting this brick

        # Drop bricks till all settled
        inair = deque(self.bricks)
        stack = defaultdict(list)  # organize bricks by zr.stop

        while inair:
            brick = inair.popleft()

            if brick.is_over_ground():
                stack[brick.zr.stop].append(brick)
                self.above[brick] = set()
                self.below[brick] = set()
                continue

            if below := {b for b in stack[brick.zr.start] if brick.is_over(b)}:
                stack[brick.zr.stop].append(brick)
                self.above[brick] = set()
                self.below[brick] = below
                for b in below:
                    self.above[b].add(brick)
                continue

            brick.drop()
            inair.append(brick)


def part1(stack):
    safe = set()

    for brick in stack.bricks:
        if not stack.above[brick] or all(
            len(stack.below[a]) > 1 for a in stack.above[brick]
        ):
            safe.add(brick)

    return len(safe)


def part2(stack):
    count = Counter()

    for target in stack.bricks:
        chain = {target}
        above = deque(stack.above[target])
        while above:
            brick = above.popleft()
            if brick in chain:
                continue
            if all(b in chain for b in stack.below[brick]):
                chain.add(brick)
                count[target] += 1
                above.extend(stack.above[brick])

    return count.total()


# noinspection DuplicatedCode
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    lines = pathlib.Path(args.f).read_text().splitlines()

    bricks = []
    for line in lines:
        numbers = [int(n) for n in re.findall(r"\d+", line)]
        bricks.append(Brick(*numbers))

    stack = Stack(bricks)

    print("part 1:", part1(stack))
    print("part 2:", part2(stack))


if __name__ == "__main__":
    main()
