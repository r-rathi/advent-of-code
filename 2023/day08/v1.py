"""Day 8: Haunted Wasteland"""

import argparse
import itertools
import math
import pathlib
import re


def part1(network, instructions):
    inst = itertools.cycle(instructions)
    node = "AAA"
    t = 0
    while node != "ZZZ":
        # print(t, node)
        node = network[node][next(inst)]
        t += 1

    return t


def part2(network, instructions):
    num_insts = len(instructions)
    start_nodes = [node for node in network if node.endswith("A")]
    periods = []
    for start_node in start_nodes:
        inst = itertools.cycle(instructions)

        states = {}
        sequence = []
        node = start_node
        t = 0
        while (node, t % num_insts) not in states:
            # print(t, t % num_insts, node)
            states[(node, t % num_insts)] = t
            sequence.append(node[-1])
            node = network[node][next(inst)]
            t += 1

        t_repeat = states[(node, t % num_insts)]

        # offset = sequence.index("Z")
        period = len(sequence) - t_repeat
        # print(offset, period)

        periods.append(period)

    return math.lcm(*periods)


# noinspection DuplicatedCode
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    insts, network_lines = pathlib.Path(args.f).read_text().split("\n\n")
    network = {}
    for line in network_lines.splitlines():
        node, left, right = re.findall(r"[A-Z0-9][A-Z0-9][A-Z]", line)
        network[node] = dict(L=left, R=right)

    print("part 1:", part1(network, insts))
    print("part 2:", part2(network, insts))


if __name__ == "__main__":
    main()
