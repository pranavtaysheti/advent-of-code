from __future__ import annotations

import fileinput
import heapq
from enum import IntEnum
from typing import NamedTuple

type Position = tuple[int, int]


class Direction(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def opp_dir(self) -> Direction:
        return Direction((self + 2) % 4)


class Orientation(IntEnum):
    VERTICAL = 0
    HORIZONTAL = 1

    @classmethod
    def get_orientation(cls, dir: Direction) -> Orientation:
        return Orientation(dir % 2)


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

    class _Seen(set[tuple[Position, Orientation]]):
        def is_seen(self, pos: Position, dir: Direction) -> bool:
            return (pos, Orientation.get_orientation(dir)) in self

        def add_dir(self, pos, dir: Direction):
            self.add((pos, Orientation.get_orientation(dir)))

    class _History(dict[Direction, tuple[int, set[Position]]]):
        def __init__(self, *args, **kwargs):
            for d in Direction:
                self[d] = 10**6, set()  # feels hacky

            super().__init__(*args, **kwargs)

    def __init__(self):
        s_pos = len(data) - 2, 1
        n_item = self._Item(cost=0, pos=s_pos, dir=Direction.EAST)

        self.end_pos = 1, len(data[1]) - 2
        self._heap: list[Solver._Item] = [n_item]
        self._seen = self._Seen()
        self._history: dict[Position, Solver._History] = {
            s_pos: self._History(
                {
                    Orientation.VERTICAL: (0, set()),
                    Orientation.HORIZONTAL: (0, set()),
                }
            )
        }

    def _move(self) -> _Item:
        item = heapq.heappop(self._heap)
        if self._seen.is_seen(item.pos, item.dir):
            return item

        row, col = item.pos

        next_items: list[tuple[Direction, Position, int]] = []
        for dir, (c_row, c_col) in VECTORS.items():
            n_pos = n_row, n_col = row + c_row, col + c_col
            if (data[n_row][n_col] == "#") or self._seen.is_seen(n_pos, dir):
                continue

            n_cost = item.cost + 1
            if dir != item.dir:
                n_cost += 1000

            next_items.append((dir, n_pos, n_cost))

        for dir, n_pos, n_cost in next_items:
            heapq.heappush(self._heap, self._Item(n_cost, n_pos, dir))

            n_data = self._history.setdefault(n_pos, self._History())
            ne_cost, _ = n_data[dir.opp_dir()]

            if n_cost < ne_cost:
                n_data[dir.opp_dir()] = (n_cost, set())

            if n_cost <= ne_cost:
                _, n_hist = n_data[dir.opp_dir()]
                for cost, hist in self._history[item.pos].values():
                    if cost == item.cost:
                        n_hist |= hist

                n_hist.add(item.pos)

        self._seen.add_dir(item.pos, item.dir)
        return item

    def solve(self) -> list[_Item]:
        while (curr := self._move()).pos != self.end_pos:
            pass

        res = [curr]

        end_cost = res[0].cost
        while (curr := self._move()).cost == end_cost:
            if curr.pos == self.end_pos:
                res.append(curr)

        return res

    def steps(self):
        res = set()
        for _, h in self._history[self.end_pos].values():
            res |= h

        return res


solver = Solver()
print(f"P1: {solver.solve()[0].cost}")
print(f"P2: {len(solver.steps())+1}")
