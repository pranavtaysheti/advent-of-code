import fileinput
from functools import cache
from typing import NamedTuple


class Node(NamedTuple):
    name: str
    connections: tuple[Node, ...]


class Graph:
    _data: dict[str, list[str]]
    _root: Node
    _end: Node
    _is_processed: bool

    def __init__(self, data: dict[str, list[str]]):
        self._data = data
        self._is_processed = False

    def _process(self):
        if self._is_processed:
            return

        nodes: dict[str, list[str]] = {}
        for n_str, con in self._data.items():
            for c in con:
                if self._data.get(c) is None:
                    nodes[c] = []

            nodes[n_str] = con

        @cache
        def build(n: str) -> Node:
            n_con = nodes[n]
            if not n_con:
                res = Node(n, ())
            else:
                res = Node(n, tuple(build(c) for c in n_con))

            return res

        self._end = build("out")
        self._root = build("you")
        self._is_processed = True

    def solve(self) -> int:
        if not self._is_processed:
            self._process()

        @cache
        def dfs(n: Node) -> int:
            if n is self._end:
                return 1

            return sum(dfs(c) for c in n.connections)

        return dfs(self._root)


def parse():
    return Graph({name[:-1]: rest for name, *rest in map(str.split, fileinput.input())})


if __name__ == "__main__":
    data = parse()
    print(f"P1: {data.solve()}")
    print(f"P2: {0}")
