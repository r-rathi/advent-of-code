"""Day 17: Clumsy Crucible"""

import argparse
import heapq
import pathlib
from operator import itemgetter
from typing import NamedTuple


def djikstra(graph, source):
    dist = {source: 0}
    prev = {source: None}

    queue = [(0, source)]  # Min dist based priority queue: [(dist, node), ...]

    while queue:
        dist_su, u = heapq.heappop(queue)

        for v, dist_uv in graph[u].items():
            dist_sv = dist_su + dist_uv
            if v not in dist or dist_sv < dist[v]:
                dist[v] = dist_sv
                prev[v] = u
                heapq.heappush(queue, (dist_sv, v))

    return dist, prev


DIRS = {
    (-1, 0): "^",
    (0, -1): "<",
    (1, 0): "v",
    (0, 1): ">",
}


class Dir(NamedTuple):
    r: int
    c: int

    def __repr__(self):
        # noinspection PyTypeChecker
        return DIRS.get(self, "x")


class Node(NamedTuple):
    position: tuple[int, int]
    direction: Dir
    steps: int

    def __repr__(self):
        return f"({self.position}, {self.direction}, {self.steps})"


class City:
    def __init__(self, map_: list[list[int]], min_steps: int, max_steps: int):
        self.R = len(map_)
        self.C = len(map_[0])
        self.min_steps = min_steps
        self.max_steps = max_steps

        self.grid = {(r, c): map_[r][c] for r in range(self.R) for c in range(self.C)}

        self.graph = {}
        for pos in self.grid:
            # Starting nodes (steps == 0)
            u = Node(pos, Dir(0, 0), 0)
            self.graph[u] = {v: self.grid[v.position] for v in self.neighbors(u)}
            # print(u, "->", self.graph[u])

            # Continuing nodes
            for direction in DIRS.keys():
                for steps in range(1, max_steps + 1):
                    u = Node(pos, Dir(*direction), steps)
                    self.graph[u] = {
                        v: self.grid[v.position] for v in self.neighbors(u)
                    }
                    # print(u, "->", self.graph[u])

    def neighbors(self, node: Node) -> list[Node]:
        (r, c), (dr, dc), steps = node

        # Starting nodes (steps == 0)
        if steps == 0:
            return [
                Node((r + dr, c + dc), Dir(dr, dc), 1)
                for dr, dc in DIRS.keys()
                if (r + dr, c + dc) in self.grid
            ]

        # Continuing nodes
        nbrs = []

        if steps < self.max_steps:
            nbrs.append(Node((r + dr, c + dc), Dir(dr, dc), steps + 1))  # Go straight

        if steps >= self.min_steps:
            nbrs.append(Node((r - dc, c + dr), Dir(-dc, dr), 1))  # Turn left
            nbrs.append(Node((r + dc, c - dr), Dir(dc, -dr), 1))  # Turn right

        return [nbr for nbr in nbrs if nbr.position in self.grid]

    def shortest_path(self, src, dst):
        dist, prev = djikstra(self.graph, source=Node(src, Dir(0, 0), 0))

        dst_nodes = [
            (n, d)
            for n, d in dist.items()
            if n.position == dst and n.steps >= self.min_steps
        ]
        dst_nodes.sort(key=itemgetter(1))
        # print(f"{dst_nodes=}")

        if not dst_nodes:
            return [], None

        goal_node, min_dist = dst_nodes[0]

        path = [goal_node]
        # noinspection PyUnresolvedReferences
        while prev_node := prev[path[0]]:
            path.insert(0, prev_node)

        return path, min_dist

    def display(self, path: list[Node]):
        p = {node.position: str(node.direction) for node in path}

        img = []
        for r in range(self.R):
            row = []
            for c in range(self.C):
                row.append(p.get((r, c), str(self.grid[r, c])))
            img.append("".join(row))

        print("\n".join(img))


def partx(city_map, min_steps, max_steps, display=False):
    city = City(city_map, min_steps, max_steps)

    lava_pool = (0, 0)
    factory = (city.R - 1, city.C - 1)

    path, distance = city.shortest_path(lava_pool, factory)

    if display:
        city.display(path)

    return distance


# noinspection DuplicatedCode
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="input.txt", help="input (default: input.txt)")
    parser.add_argument("-d", action="store_true", help="display")
    args = parser.parse_args()

    lines = pathlib.Path(args.f).read_text().splitlines()
    city_map = [[int(n) for n in line] for line in lines]

    print("part 1:", partx(city_map, min_steps=1, max_steps=3, display=args.d))
    print("part 2:", partx(city_map, min_steps=4, max_steps=10, display=args.d))


if __name__ == "__main__":
    main()
