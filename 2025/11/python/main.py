import fileinput
from functools import cache
from typing import NamedTuple


class Node(NamedTuple):
    name: str
    connections: tuple[Node, ...]


class Graph:
    _data: dict[str, list[str]]
    _is_processed: bool
    _nodes: dict[str, list[str]]

    def __init__(self, data: dict[str, list[str]]):
        self._data = data
        self._is_processed = False

    def _process(self):
        if self._is_processed:
            return

        self._nodes = {}
        for n_str, con in self._data.items():
            for c in con:
                if self._data.get(c) is None:
                    self._nodes[c] = []

            self._nodes[n_str] = con

        self._is_processed = True

    def _build(self, root: str, end: str = "out") -> tuple[Node, Node]:
        @cache
        def build(n: str) -> Node:
            n_con = self._nodes[n]
            if not n_con:
                res = Node(n, ())
            else:
                res = Node(n, tuple(build(c) for c in n_con))

            return res

        return build(root), build(end)

    def solve(self, start: str) -> int:
        if not self._is_processed:
            self._process()

        root, end = self._build(start)

        @cache
        def dfs(n: Node) -> int:
            if n is end:
                return 1

            return sum(dfs(c) for c in n.connections)

        return dfs(root)


def parse():
    return Graph({name[:-1]: rest for name, *rest in map(str.split, fileinput.input())})


if __name__ == "__main__":
    data = parse()
    print(f"P1: {data.solve("you")}")
    print(f"P2: {0}")
