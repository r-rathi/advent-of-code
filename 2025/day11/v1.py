"""Day 11: Reactor

For part 1, I initially implemented general all-path enumeration based on DFS.
However, as expected, it failed for part 2 because in general the number of
paths can be very large ~ O(n!).

After a lot(!) of side-quests trying to simplify the graph and handle cycles,
I randomly decided to actually check the input graph and realized that it is a DAG!
With this information, a DFS based direct path counting solution solved both parts.

NB: Claude helped generalize the intermediate node tracking idea for part 2.


References:
- https://networkx.org/documentation/stable/reference/algorithms/simple_paths.html

Tags: #dag #dfs #memoization #path-counting #path-enumeration #frozenset-state #llm
"""

import functools
from typing import Iterator

type Node = str
type Graph = dict[Node, set[Node]]
type Path = list[Node]


def enumerate_all_paths(
    graph: Graph, start: Node, targets: set[Node]
) -> Iterator[Path]:
    """Enumerate all simple paths from start to any target node"""
    if start not in graph:
        return

    def dfs(path: Path) -> Iterator[Path]:
        node = path[-1]
        if node in targets:
            yield path
        for neighbor in graph[node]:
            if neighbor not in path:
                yield from dfs(path + [neighbor])

    yield from dfs([start])


def count_all_paths(
    dag: Graph, start: Node, targets: set[Node], through: set[Node]
) -> int:
    """Count all paths in a DAG from start to any target node through ALL nodes in 'through'"""
    if start not in dag:
        return 0

    @functools.cache
    def dfs(node: Node, remaining: frozenset[Node]) -> int:
        # Mark this node as visited if it's a required through node
        remaining = remaining - {node}

        if node in targets:
            # Only count if we've passed through all required nodes
            return 1 if not remaining else 0
        return sum(dfs(neighbor, remaining) for neighbor in dag[node])

    return dfs(start, frozenset(through))


def part1(graph: Graph, enumerate_paths: bool = False) -> int:
    if enumerate_paths:
        print("enumerating paths from 'you' to 'out'")
        num_paths = 0
        for path in enumerate_all_paths(graph, "you", {"out"}):
            print(path)
            num_paths += 1
        print(f"enumerated {num_paths} paths from 'you' to 'out'")

    return count_all_paths(graph, "you", {"out"}, set())


def part2(graph: Graph) -> int:
    return count_all_paths(graph, "svr", {"out"}, {"dac", "fft"})


def main() -> None:
    import argparse
    import pathlib

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    parser.add_argument("-e", action="store_true", help="enumerate paths")
    args = parser.parse_args()

    lines = pathlib.Path(args.f).read_text().splitlines()

    graph: Graph = {}
    for line in lines:
        node, *neighbors = line.replace(":", "").split()
        graph[node] = set(neighbors)
        for neighbor in neighbors:
            graph.setdefault(neighbor, set())

    print("part 1 count:", part1(graph, enumerate_paths=args.e))
    print("part 2 count:", part2(graph))


if __name__ == "__main__":
    main()
