import fileinput
from itertools import combinations
from math import prod, sqrt
from typing import Iterable, NamedTuple, Sequence


class Position(NamedTuple):
    x: int
    y: int
    z: int


class Graph:
    _nodes: dict[Position, int]
    _sorted_pairs: Sequence[tuple[Position, Position, float]] | None
    _curr: int
    _sub_graphs: dict[int, set[Position]]

    def __init__(self, pos: Iterable[Position]):
        self._sorted_pairs = None
        self._sub_graphs = {i: set([p]) for i, p in enumerate(pos)}
        self._nodes = {p: i for i, p in enumerate(pos)}
        self._curr = 0

    def _process(self):
        if isinstance(self._sorted_pairs, list):
            return

        self._sorted_pairs = sorted(
            [(p1, p2, distance(p1, p2)) for p1, p2 in combinations(self._nodes, 2)],
            key=lambda e: e[2],
        )

    def _connect(self):
        assert self._sorted_pairs is not None

        p1, p2, _ = self._sorted_pairs[self._curr]
        sg1, sg2 = self._nodes[p1], self._nodes[p2]
        self._curr += 1

        if sg1 == sg2:
            return

        else:
            self._nodes[p1] = sg2
            for node in self._sub_graphs[sg1]:
                self._nodes[node] = sg2

            self._sub_graphs[sg2].update(self._sub_graphs[sg1])
            self._sub_graphs.pop(sg1)

    def connect_for(self, lim: int):
        self._process()
        assert self._sorted_pairs is not None

        for _ in range(lim):
            self._connect()

    def connect_until(self) -> tuple[Position, Position]:
        self._process()
        assert self._sorted_pairs is not None

        while len(self._sub_graphs) > 1:
            self._connect()

        return self._sorted_pairs[self._curr - 1][:2]

    def score(self):
        return sorted([len(v) for v in self._sub_graphs.values()], reverse=True)


def distance(p1: Position, p2: Position) -> float:
    return sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2 + (p2.z - p1.z) ** 2)


def parse() -> list[Position]:
    return [Position(*[int(n) for n in l[:-1].split(",")]) for l in fileinput.input()]


if __name__ == "__main__":
    graph = Graph(parse())

    graph.connect_for(1000)
    print(f"P1: {prod(graph.score()[:3])}")

    last = graph.connect_until()
    print(f"P2: {last[0].x*last[1].x}")
