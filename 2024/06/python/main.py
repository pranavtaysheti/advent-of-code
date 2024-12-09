import fileinput
from copy import copy
from dataclasses import InitVar
from enum import IntEnum
from typing import Callable, Literal, NamedTuple, Self


class Vector(NamedTuple):
    c_row: Literal[-1, 0, +1]
    c_col: Literal[-1, 0, +1]


class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Position(NamedTuple):
    row: int
    col: int


class Cursor:
    def __init__(self, pos: Position, direction: Direction):
        self._position: Position = pos
        match direction:
            case Direction.UP:
                self._vector = Vector(-1, 0)
            case Direction.RIGHT:
                self._vector = Vector(0, +1)
            case Direction.DOWN:
                self._vector = Vector(+1, 0)
            case Direction.LEFT:
                self._vector = Vector(0, -1)

    @property
    def position(self):
        return self._position

    @property
    def vector(self):
        return self._vector

    def turn(self):
        self._vector = Vector(self._vector.c_col, -self._vector.c_row)

    def step(self):
        row, col = self._position
        c_row, c_col = self._vector
        self._position = Position(row + c_row, col + c_col)


class Region(list[list[bool]]):
    def guard_path(self, curr: Cursor) -> tuple[set[Position], bool]:
        curr = copy(curr)
        res: set[Position] = set()
        obstacles: dict[Position, list[Vector]] = {}

        while (0 <= (row := curr.position.row) < len(self)) and (
            0 <= (col := curr.position.col) < len(self[row])
        ):
            while (
                0 <= (n_row := row + curr.vector.c_row) < len(self)
                and 0 <= (n_col := col + curr.vector.c_col) < len(self[n_row])
                and self[n_row][n_col]
            ):

                pos = Position(n_row, n_col)
                obstacles.setdefault(pos, [])

                if curr.vector in obstacles[pos]:
                    return res, True

                obstacles[pos].append(curr.vector)
                curr.turn()

            res.add(curr.position)
            curr.step()

        return res, False

    def set_obstacle(self, pos: Position, func: Callable, *args, **kwargs):
        self[pos.row][pos.col] = True
        res = func(*args, **kwargs)
        self[pos.row][pos.col] = False
        return res


start: Cursor | None = None
data: Region = Region()

CURSOR_SYM: dict[str, Direction] = {
    "^": Direction.UP,
    ">": Direction.RIGHT,
    "v": Direction.DOWN,
    "<": Direction.LEFT,
}

with fileinput.input() as file:
    for i, line in enumerate(file):
        parsed_line: list[bool] = []
        for j, c in enumerate(line):
            if c == "#":
                parsed_line.append(True)
            else:
                parsed_line.append(False)

            if c in ["^", ">", "<", "v"]:
                start = Cursor(Position(i, j), CURSOR_SYM[c])

        data.append(parsed_line)

assert isinstance(start, Cursor)
guard_pos, _ = data.guard_path(start)

print(f"P1: {len(guard_pos)}")
print(f"P2: {[data.set_obstacle(pos, data.guard_path,start)[1] for pos in guard_pos].count(True)}")
