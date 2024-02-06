"""Day 25: Snowverload

    Minimum (edge) cut problem
    https://en.wikipedia.org/wiki/Minimum_cut

    Stoer-Wagner Algorithm
    - https://en.wikipedia.org/wiki/Stoer–Wagner_algorithm
    - https://dl.acm.org/doi/abs/10.1145/263867.263872

    Tags: #min-cut #stoer-wagner
    Tags: #networkx

"""

import argparse
import pathlib
from math import prod

import networkx as nx


def part1(G):
    cut_value, partitions = nx.stoer_wagner(G)
    assert cut_value == 3, cut_value
    assert len(partitions) == 2, partitions
    # print(cut_value)
    # print(partitions)
    # print([len(p) for p in partitions])
    return prod(len(p) for p in partitions)


# noinspection DuplicatedCode
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    lines = pathlib.Path(args.f).read_text().splitlines()

    G = nx.Graph()
    for line in lines:
        u, *vs = line.split()
        u = u[:-1]
        for v in vs:
            G.add_edge(u, v)

    # for v in G:
    #     print(v, G[v])
    # print(G)

    print("part 1:", part1(G))


if __name__ == "__main__":
    main()
