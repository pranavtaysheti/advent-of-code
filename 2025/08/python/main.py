import fileinput
from itertools import combinations
from math import prod
from typing import Iterable, NamedTuple


class Position(NamedTuple):
    x: int
    y: int
    z: int


type Connection = tuple[Node, Node, int]


class Node:
    def __init__(self, pos: Position) -> None:
        self.pos: Position = pos
        self.group: list[Node] = [self]


class Graph:
    def __init__(self, pos: Iterable[Position]):
        self._sorted_pairs: None | list[Connection] = None
        self._nodes: list[Node] = [Node(p) for p in pos]
        self._curr: int = 0
        self._groups: int = len(self._nodes)

    def _process(self):
        if self._sorted_pairs is not None:
            return

        self._sorted_pairs = sorted(
            [
                (p1, p2, distance(p1.pos, p2.pos))
                for p1, p2 in combinations(self._nodes, 2)
            ],
            key=lambda e: e[2],
        )

    def _connect(self):
        assert self._sorted_pairs is not None
        assert self._curr < len(
            self._sorted_pairs
        ), "Make sure you are not iterating too much"

        n1, n2, _ = self._sorted_pairs[self._curr]
        self._curr += 1

        if n1.group is n2.group:
            return

        else:
            if len(n1.group) < len(n2.group):
                min_group = n1.group
                max_group = n2.group
            else:
                min_group = n2.group
                max_group = n1.group

            max_group.extend(min_group)
            for n in min_group:
                n.group = max_group

            self._groups -= 1

    def connect_for(self, lim: int):
        self._process()
        assert self._sorted_pairs is not None

        for _ in range(lim):
            self._connect()

    def connect_until(self) -> tuple[Position, Position]:
        self._process()
        assert self._sorted_pairs is not None

        while self._groups > 1:
            self._connect()

        n1, n2 = self._sorted_pairs[self._curr - 1][:2]
        return n1.pos, n2.pos

    def score(self):
        return sorted(
            list({id(n.group): len(n.group) for n in self._nodes}.values()),
            reverse=True,
        )


def distance(p1: Position, p2: Position) -> int:
    return (p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2 + (p2.z - p1.z) ** 2


def parse() -> list[Position]:
    return [Position(*[int(n) for n in l[:-1].split(",")]) for l in fileinput.input()]


if __name__ == "__main__":
    graph = Graph(parse())

    graph.connect_for(1000)
    print(f"P1: {prod(graph.score()[:3])}")

    last = graph.connect_until()
    print(f"P2: {last[0].x*last[1].x}")
