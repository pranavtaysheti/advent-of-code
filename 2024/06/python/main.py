import fileinput
from copy import copy
from dataclasses import InitVar, dataclass
from enum import IntEnum
from typing import Literal, NamedTuple


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


@dataclass
class Cursor:
    position: Position
    direction: InitVar[Direction]

    def __post_init__(self, direction):
        match direction:
            case Direction.UP:
                self.vector = Vector(-1, 0)
            case Direction.RIGHT:
                self.vector = Vector(0, +1)
            case Direction.DOWN:
                self.vector = Vector(+1, 0)
            case Direction.LEFT:
                self.vector = Vector(0, -1)

    def turn(self):
        self.vector = Vector(self.vector.c_col, -self.vector.c_row)

    def step(self):
        row, col = self.position
        c_row, c_col = self.vector
        self.position = Position(row + c_row, col + c_col)


class Region(list[list[bool]]):
    def is_mapped(self, row: int, col: int):
        return 0 <= row < len(self) and 0 <= col < len(self[0])

    def guard_path(self) -> tuple[set[Position], bool]:
        assert isinstance(start, Cursor)
        curr: Cursor = copy(start)

        res: set[Position] = set()
        obstacles: dict[Position, list[Vector]] = {}

        while self.is_mapped(row := curr.position.row, col := curr.position.col):
            while (
                self.is_mapped(
                    n_row := row + curr.vector.c_row,
                    n_col := col + curr.vector.c_col,
                )
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

guard_pos, _ = data.guard_path()
print(f"P1: {len(guard_pos)}")

P2 = 0
for row, col in guard_pos:
    if (row, col) == start.position:
        continue

    data[row][col] = True
    P2 += data.guard_path()[1]
    data[row][col] = False

print(f"P2: {P2}")
