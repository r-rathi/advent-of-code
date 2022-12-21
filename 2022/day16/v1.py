"""Day 16: Proboscidea Volcanium"""
import pathlib
import re
import sys
from functools import cache
from typing import Tuple


def shortest_distance(graph, inf=int(1e6)):
    # Floyd–Warshall algorithm: https://en.wikipedia.org/wiki/Floyd–Warshall_algorithm
    distance = {}
    for src in graph:
        for dst in graph:
            if src == dst:
                distance[(src, dst)] = 0
            elif dst in graph[src]:
                distance[(src, dst)] = 1
            else:
                distance[(src, dst)] = inf

    for mid in graph:
        for src in graph:
            for dst in graph:
                distance[(src, dst)] = min(
                    distance[(src, dst)], distance[(src, mid)] + distance[(mid, dst)]
                )

    # print("All-pair shortest distances:")
    # print("   ", end="")
    # for dst in graph:
    #     print(f" {dst:3s}", end="")
    # print()
    # for src in graph:
    #     print(f"{src}", end="")
    #     for dst in graph:
    #         print(f" {distance[(src, dst)]:3d}", end="")
    #     print()

    return distance


class ValveNetwork:
    def __init__(self, graph: dict[str, list[str]], rates: dict[str, int], start: str, timeout: int):
        self.graph = graph
        self.rates = rates
        self.dists = shortest_distance(self.graph)
        self.start = start
        self.timeout = timeout

    @cache
    def open1(self, current: str, closed: Tuple[str], time: int) -> Tuple[int, list]:
        if time == 0:
            return 0, []

        max_flow = 0
        best_seq = []

        for i, first_valve in enumerate(closed):
            remaining_time = time - self.dists[(current, first_valve)] - 1
            if remaining_time > 0:
                remaining_valves = tuple(closed[:i] + closed[i + 1:])

                flow0 = remaining_time * self.rates[first_valve]
                flow1, seq1 = self.open1(first_valve, remaining_valves, remaining_time)

                if flow0 + flow1 > max_flow:
                    max_flow = flow0 + flow1
                    best_seq = [first_valve] + seq1

        return max_flow, best_seq

    @cache
    def open2(self, current: str, closed: Tuple[str], time: int) -> Tuple[int, list]:
        if time == 0:
            return 0, []

        max_flow = 0
        best_seq = []

        for i, first_valve in enumerate(closed):
            remaining_time = time - self.dists[(current, first_valve)] - 1
            if remaining_time > 0:
                remaining_valves = tuple(closed[:i] + closed[i + 1:])

                flow0 = remaining_time * self.rates[first_valve]
                flow1, seq1 = self.open1(self.start, remaining_valves, self.timeout)
                flow2, seq2 = self.open2(first_valve, remaining_valves, remaining_time)

                if flow1 > flow2:
                    if flow0 + flow1 > max_flow:
                        max_flow = flow0 + flow1
                        best_seq = [first_valve]
                else:
                    if flow0 + flow2 > max_flow:
                        max_flow = flow0 + flow2
                        best_seq = [first_valve] + seq2

        return max_flow, best_seq


def part1(graph, rates):
    valves = ValveNetwork(graph, rates, "AA", 30)

    closed = tuple(v for v in valves.graph if valves.rates[v] > 0)

    max_flow, best_seq = valves.open1(valves.start, closed, valves.timeout)

    print("max_flow:", max_flow)
    print("best_seq:", best_seq)

    return max_flow


def part2(graph, rates):
    valves = ValveNetwork(graph, rates, "AA", 26)

    closed = tuple(v for v in valves.graph if valves.rates[v] > 0)

    max_flow, best_seq = valves.open2(valves.start, closed, valves.timeout)

    max_flow2, best_seq2 = valves.open1(valves.start, tuple(set(closed) - set(best_seq)), valves.timeout)
    max_flow1, best_seq1 = valves.open1(valves.start, tuple(set(closed) - set(best_seq2)), valves.timeout)

    assert max_flow1 + max_flow2 == max_flow
    assert best_seq1 == best_seq

    print("max_flow:", max_flow1, "+", max_flow2, "=", max_flow)
    print("best_seq:", best_seq1, best_seq2)

    return max_flow


def main():
    if len(sys.argv) == 1:
        input_file = "input.txt"
    else:
        input_file = sys.argv[1]

    lines = pathlib.Path(input_file).read_text().splitlines()

    graph = {}
    rates = {}
    for line in lines:
        valves = re.findall(r"[A-Z]{2}", line)
        flow = int(re.search(r"\d+", line)[0])
        graph[valves[0]] = valves[1:]
        rates[valves[0]] = flow

    print("part 1:", part1(graph, rates))
    print("part 2:", part2(graph, rates))


if __name__ == "__main__":
    main()
