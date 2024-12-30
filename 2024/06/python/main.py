import fileinput
from collections.abc import Callable
from copy import copy
from typing import Literal, NamedTuple


class Vector(NamedTuple):
    c_row: Literal[-1, 0, +1]
    c_col: Literal[-1, 0, +1]


class Position(NamedTuple):
    row: int
    col: int


class Cursor:
    def __init__(self, pos: Position, vector: Vector):
        self.position: Position = pos
        self.vector = vector

    def turn(self):
        self.vector = Vector(self.vector.c_col, -self.vector.c_row)

    def next_pos(self) -> Position:
        row, col = self.position
        c_row, c_col = self.vector
        return Position(row + c_row, col + c_col)


class Region(list[list[bool]]):
    def guard_path(self, curr: Cursor) -> tuple[set[Position], bool]:
        curr = copy(curr)
        res: set[Position] = set()
        obstacles: dict[Position, set[Vector]] = {}

        def is_inside(pos: Position) -> bool:
            return 0 <= pos.row < len(self) and 0 <= pos.col < len(self[pos.row])

        while is_inside(curr.position):
            while is_inside(n_pos := curr.next_pos()) and self[n_pos.row][n_pos.col]:
                if curr.vector in (seen_vectors := obstacles.setdefault(n_pos, set())):
                    return res, True

                seen_vectors.add(curr.vector)
                curr.turn()

            res.add(curr.position)
            curr.position = n_pos

        return res, False

    def set_obstacle(self, pos: Position, func: Callable, *args, **kwargs):
        self[pos.row][pos.col] = True
        res = func(*args, **kwargs)
        self[pos.row][pos.col] = False
        return res


start: Cursor | None = None
data: Region = Region()

with fileinput.input() as file:
    for i, line in enumerate(file):
        parsed_line: list[bool] = []
        for j, c in enumerate(line[:-1]):
            if c == "#":
                parsed_line.append(True)
            else:
                parsed_line.append(False)

                if c == ".":
                    continue

                match c:
                    case "^":
                        vec = Vector(-1, 0)
                    case ">":
                        vec = Vector(0, +1)
                    case "v":
                        vec = Vector(+1, 0)
                    case "<":
                        vec = Vector(0, -1)
                    case _:
                        raise AssertionError(f"unparsable char: {c}")

                start = Cursor(Position(i, j), vec)

        data.append(parsed_line)

assert isinstance(start, Cursor)
guard_pos, _ = data.guard_path(start)

print(f"P1: {len(guard_pos)}")
print(
    f"P2: {[data.set_obstacle(pos, data.guard_path,start)[1] for pos in guard_pos].count(True)}"
)
