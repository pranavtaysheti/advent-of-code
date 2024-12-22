from __future__ import annotations

import fileinput
from dataclasses import dataclass
from enum import Enum, IntEnum
from heapq import heappop, heappush
from typing import Literal, NamedTuple

type VectorComponent = Literal[-1, 0, +1]
type Vector = tuple[VectorComponent, VectorComponent]


class Position(NamedTuple):
    row: int
    col: int

    def add_vector(self, vector: Vector) -> Position:
        c_row, c_col = vector
        return Position(self.row + c_row, self.col + c_col)


class Orientation(Enum):
    VERTICAL = 0
    HORIZONTAL = 1


class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def turn(self) -> list[Direction]:
        return [Direction((self - 1) % 4), Direction((self + 1) % 4)]

    def vector(self) -> Vector:
        match self:
            case Direction.UP:
                return (-1, 0)
            case Direction.RIGHT:
                return (0, +1)
            case Direction.DOWN:
                return (+1, 0)
            case Direction.LEFT:
                return (0, -1)

    def orientation(self) -> Orientation:
        return Orientation(self % 2)


@dataclass
class City:
    class HeapItem(NamedTuple):
        dist: int
        pos: Position
        dir: Direction
        l_stp: int

    class Seen(dict[tuple[Position, Orientation], int]):
        def __init__(self, min_turn: int):
            self.min_turn = min_turn
            super().__init__()

        def evaluate(
            self, pos: Position, dir: Direction, l_stp: int
        ) -> tuple[bool, bool]:
            """is_seen
            0: if orientation is seen - if false - Dont turn
            1: if l_stp is lower than seen l_stp - if false - Dont go ahead.
            """

            if (v := (pos, dir.orientation())) in self:
                if l_stp >= self[v]:
                    return False, False

                else:
                    if l_stp >= self.min_turn:
                        self[v] = l_stp

                    return False, True

            else:
                if l_stp >= self.min_turn:
                    self[v] = l_stp
                return True, True

    layout: list[list[int]]

    def solve(self, min_turn: int, max_linear: int) -> int:
        heap: list[City.HeapItem] = []
        seen: City.Seen = self.Seen(min_turn)

        heappush(heap, self.HeapItem(0, Position(0, 0), Direction.RIGHT, 0))

        while len(heap) > 0:
            curr = heappop(heap)
            if curr.pos == Position(len(self.layout) - 1, len(self.layout[0]) - 1):
                return curr.dist

            to_turn, to_continue = seen.evaluate(*curr[1:])
            next: list[tuple[Position, Direction, int]] = []

            if to_turn and curr.l_stp >= min_turn:
                for d in curr.dir.turn():
                    next.append((curr.pos.add_vector(d.vector()), d, 1))

            if to_continue and curr.l_stp < max_linear:
                next.append(
                    (curr.pos.add_vector(curr.dir.vector()), curr.dir, curr.l_stp + 1)
                )

            for pos, dir, l_stp in next:
                if (0 <= pos.row < len(self.layout)) and (
                    0 <= pos.col < len(self.layout[pos.row])
                ):
                    dist = curr.dist + self.layout[pos.row][pos.col]
                    heappush(heap, self.HeapItem(dist, pos, dir, l_stp))

        raise AssertionError(f"No solution found!")


data: City = City([])

with fileinput.input() as input_file:
    for line in input_file:
        data.layout.append([int(c) for c in line[:-1]])

print(f"P1: {data.solve(1, 3)}")
print(f"P2: {data.solve(4,10)}")
