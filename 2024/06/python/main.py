import fileinput
from copy import copy
from dataclasses import dataclass
from enum import IntEnum
from typing import NamedTuple


class Vector(NamedTuple):
    c_row: int
    c_col: int


class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Position(NamedTuple):
    row: int
    col: int


@dataclass
class Cursor:
    position: Position
    direction: Direction

    def __post_init__(self):
        match self.direction:
            case Direction.UP:
                self.vector = Vector(-1, 0)
            case Direction.RIGHT:
                self.vector = Vector(0, +1)
            case Direction.DOWN:
                self.vector = Vector(+1, 0)
            case Direction.LEFT:
                self.vector = Vector(0, -1)

    def turn(self):
        self.direction = Direction((self.direction.value + 1) % 4)
        self.vector = Vector(self.vector.c_col, -self.vector.c_row)

    def step(self):
        row, col = self.position
        c_row, c_col = self.vector
        self.position = Position(row + c_row, col + c_col)


class Region(list[list[bool]]):
    def guard_path(self) -> set[Position]:
        assert isinstance(start, Cursor)
        curr: Cursor = copy(start)
        res: set[Position] = set()

        while self.is_mapped(row := curr.position.row, col := curr.position.col):
            c_row, c_col = curr.vector
            if self.is_mapped(n_row := row + c_row, n_col := col + c_col):
                if self[n_row][n_col]:
                    curr.turn()

            res.add(curr.position)
            curr.step()

        return res

    def is_mapped(self, row: int, col: int):
        return 0 <= row < len(self) and 0 <= col < len(self[0])


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

print(f"P1: {len(data.guard_path())}")
print(f"P2: {0}")
