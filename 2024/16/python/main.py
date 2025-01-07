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
    class Item(NamedTuple):
        cost: int
        pos: Position
        dir: Direction

    class Seen(set[tuple[Position, int]]):
        def check(self, pos: Position, dir: Direction) -> bool:
            return not (pos, dir % 2) in self

    def __init__(self):
        self.heap: list[Solver.Item] = [
            self.Item(cost=0, pos=(len(data) - 2, 1), dir=Direction.EAST)
        ]
        self.seen: Solver.Seen = self.Seen()

    def move(self) -> Item:
        item = heapq.heappop(self.heap)

        if (item.pos, item.dir % 2) in self.seen:
            return item

        self.seen.add((item.pos, item.dir % 2))
        row, col = item.pos

        for dir, (c_row, c_col) in VECTORS.items():
            n_pos = n_row, n_col = row + c_row, col + c_col

            if data[n_row][n_col] != "#":
                n_cost = item.cost + 1
                if dir != item.dir:
                    n_cost += 1000

                if self.seen.check(n_pos, dir):
                    heapq.heappush(self.heap, self.Item(n_cost, n_pos, dir))

        return item

    def solve(self) -> Item:
        end_pos = 1, len(data[1]) - 2
        while (curr := self.move()).pos != end_pos:
            pass

        return curr


print(f"P1: {Solver().solve().cost}")
print(f"P2: {0}")
