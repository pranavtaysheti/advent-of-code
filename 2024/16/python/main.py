from __future__ import annotations

import fileinput
import heapq
from enum import IntEnum
from functools import cache
from itertools import chain
from typing import NamedTuple

type Position = tuple[int, int]


class Direction(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


VECTORS: dict[Direction, Position] = {
    Direction.NORTH: (-1, 0),
    Direction.EAST: (0, +1),
    Direction.SOUTH: (+1, 0),
    Direction.WEST: (0, -1),
}

data: list[str] = []

with fileinput.input() as input_file:
    for line in input_file:
        data.append(line[:-1])


class Solver:
    class _Item(NamedTuple):
        cost: int
        pos: Position
        dir: Direction

    class _Seen(set[tuple[Position, int]]):
        def is_seen(self, pos: Position, dir: Direction) -> bool:
            return (pos, dir % 2) in self

    def __init__(self):
        s_pos = len(data) - 2, 1
        n_item = self._Item(cost=0, pos=s_pos, dir=Direction.EAST)

        self.end_pos = 1, len(data[1]) - 2
        self._heap: list[Solver._Item] = [n_item]
        self._history: dict[Position, list[list[Position]]] = {s_pos: [[]]}
        self._seen = self._Seen()

    def _move(self) -> _Item:
        item = heapq.heappop(self._heap)

        if self._seen.is_seen(item.pos, item.dir):
            return item

        self._seen.add((item.pos, item.dir % 2))
        row, col = item.pos

        for dir, (c_row, c_col) in VECTORS.items():
            n_pos = n_row, n_col = row + c_row, col + c_col

            if data[n_row][n_col] == "#":
                continue

            n_cost = item.cost + 1
            if dir != item.dir:
                n_cost += 1000

            if not self._seen.is_seen(n_pos, dir):
                heapq.heappush(self._heap, self._Item(n_cost, n_pos, dir))

                hist = self._history[item.pos]
                min_len = min(len(h) for h in hist)
                n_hist = [h.copy() for h in hist if len(h) == min_len]

                for h in n_hist:
                    h.append(item.pos)

                self._history.setdefault(n_pos, []).extend(n_hist)

        return item

    @cache
    def solve(self) -> list[_Item]:
        while (curr := self._move()).pos != self.end_pos:
            pass

        res = [curr]

        end_cost = res[0].cost
        while (curr := self._move()).cost == end_cost:
            if curr.pos == self.end_pos:
                res.append(curr)

        return res

    @cache
    def steps(self):
        return set(chain.from_iterable(self._history[self.end_pos]))

    def print_steps(self):
        res = [[c for c in r] for r in data]
        for row, col in self.steps():
            res[row][col] = "O"

        print("\n".join("".join(c for c in r) for r in res))


solver = Solver()
print(f"P1: {solver.solve()[0].cost}")
print(f"P2: {len(solver.steps())}")
