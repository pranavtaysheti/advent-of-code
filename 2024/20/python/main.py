from __future__ import annotations

import fileinput
from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum
from itertools import combinations
from typing import Literal


@dataclass(frozen=True)
class Vector:
    row: int
    col: int

    def __add__(self, v: Vector) -> Vector:
        return Vector(self.row + v.row, self.col + v.col)

    def __sub__(self, v: Vector) -> Vector:
        return Vector(self.row - v.row, self.col - v.col)

    def distance(self) -> int:
        return abs(self.row) + abs(self.col)

    def tuple(self) -> tuple[int, int]:
        return (self.row, self.col)


class Direction(Vector, Enum):
    NORTH = -1, 0
    EAST = 0, 1
    SOUTH = +1, 0
    WEST = 0, -1


class RaceTrack:
    def __init__(self, data: Iterable[str]):
        self.data: list[list[int | Literal["W"]]] = []
        self.track: list[Vector] = []

        num_mapper = lambda c: "W" if c == "#" else 0

        for row, line in enumerate(data):
            if (i := line[:-1].find("S")) > -1:
                self.start = Vector(row, i)
            if (i := line[:-1].find("E")) > -1:
                self.end = Vector(row, i)

            self.data.append([num_mapper(c) for c in line])

        self._prime()

    def _prime(self):
        self.track.append(self.start)

        curr: Vector = self.start
        prev: Vector | None = None
        curr_num = 0
        while curr != self.end:
            curr_num += 1
            for d in Direction:
                n_pos = curr + d
                n_row, n_col = n_pos.tuple()
                if self.data[n_row][n_col] != 0 or n_pos == prev:
                    continue

                self.track.append(n_pos)
                self.data[n_row][n_col] = curr_num
                prev = curr
                curr = n_pos
                break

    def find_cheats(self, time: int) -> dict[tuple[Vector, Vector], int]:
        res: dict[tuple[Vector, Vector], int] = {}
        for v1, v2 in combinations(self.track, 2):
            (v1_row, v1_col), (v2_row, v2_col) = v1.tuple(), v2.tuple()

            v1_cost, v2_cost = self.data[v1_row][v1_col], self.data[v2_row][v2_col]
            assert isinstance(v1_cost, int)
            assert isinstance(v2_cost, int)

            if ((dist := (v1 - v2).distance()) <= time) and (
                abs(v1_cost - v2_cost) > dist
            ):
                cost = abs(v1_cost - v2_cost) - dist
                res[v1, v2] = cost

        return res


race = RaceTrack(l[:-1] for l in fileinput.input(encoding="utf-8"))

print(f"P1: {sum(1 for v in race.find_cheats(2).values() if v >= 100)}")
print(f"P2: {sum(1 for v in race.find_cheats(20).values() if v >= 100)}")
