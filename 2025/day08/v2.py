"""Day 8: Playground

This puzzle is essentially the connected component or the minimum spanning
forest/tree problem.

Kruskal's algorithm finds the minimum spanning forest. Starting from single node
components, edges are added in the increasing order of weight if adding the edge
will not create a cycle, i.e., the edge connects nodes belonging to two different
components. Algorithm uses the tree based disjoint set union datastructure (also
known as union-find) to keep track of the components and their unions.

References:
- https://en.wikipedia.org/wiki/Component_(graph_theory)
- https://en.wikipedia.org/wiki/Minimum_spanning_tree
- https://en.wikipedia.org/wiki/Kruskal%27s_algorithm
- https://en.wikipedia.org/wiki/Disjoint-set_data_structure

Tags: #connected-component #minimum-spanning-tree #kruskals-algorithm
Tags: #disjoint-set #union-find
Tags: #llm

NB: While union find optimizes the core part of the algorithm, the total run
    time is dominated by the edge sorting step!

"""

import math
from typing import NamedTuple


class Node(NamedTuple):
    x: int
    y: int
    z: int


class Edge(NamedTuple):
    u: Node
    v: Node
    w: int


def make_edge(u: Node, v: Node) -> Edge:
    dx = u.x - v.x
    dy = u.y - v.y
    dz = u.z - v.z
    w = dx * dx + dy * dy + dz * dz
    return Edge(u, v, w)


class UnionFind:
    def __init__(self, nodes: list[Node]) -> None:
        self.parent = {v: v for v in nodes}
        self.size = {v: 1 for v in nodes}
        self.num_components = len(nodes)

    def find(self, u: Node) -> Node:
        if self.parent[u] != u:
            # Path compression: point directly to the root
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u: Node, v: Node) -> bool:
        """Returns True if a merge occurred."""
        ru, rv = self.find(u), self.find(v)
        if ru == rv:
            return False

        # Union by size: attach smaller tree under larger tree
        if self.size[ru] < self.size[rv]:
            ru, rv = rv, ru
        self.parent[rv] = ru
        self.size[ru] += self.size[rv]

        self.num_components -= 1
        return True

    def component_sizes(self) -> list[int]:
        return [self.size[v] for v in self.parent if v == self.parent[v]]


def part1(nodes: list[Node], edges: list[Edge], max_connections: int) -> int:
    uf = UnionFind(nodes)

    for i, e in enumerate(edges):
        if i >= max_connections:
            break
        uf.union(e.u, e.v)

    sizes = sorted(uf.component_sizes(), reverse=True)
    return math.prod(sizes[:3])


def part2(nodes: list[Node], edges: list[Edge]) -> int:
    uf = UnionFind(nodes)

    for e in edges:
        if uf.union(e.u, e.v) and uf.num_components == 1:
            return e.u.x * e.v.x

    return -1


def main():
    # noinspection DuplicatedCode
    import argparse
    import pathlib

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    args = parser.parse_args()

    max_connections = 1000 if args.f == "input.txt" else 10

    lines = pathlib.Path(args.f).read_text().splitlines()

    nodes = [Node(*map(int, line.split(","))) for line in lines]
    edges = [make_edge(u, v) for i, u in enumerate(nodes) for v in nodes[i + 1 :]]

    # NB: this is the real bottleneck!
    edges.sort(key=lambda e: e.w)

    print("part 1:", part1(nodes, edges, max_connections))
    print("part 2:", part2(nodes, edges))


if __name__ == "__main__":
    main()
