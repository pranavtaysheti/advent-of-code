import fileinput
from enum import Enum, auto
from itertools import groupby, pairwise
from math import ceil
from re import T
from typing import NamedTuple, NoReturn


class NonContinuousPipeError(ValueError):
    pass


class Coordinate(NamedTuple):
    row: int
    column: int


class Direction(Enum):
    North = auto()
    South = auto()
    East = auto()
    West = auto()


class Pipe(NamedTuple):
    ends: tuple[Direction, Direction] | None


class StartPipe(Pipe):
    pass


PIPETYPE: dict[str, Pipe] = {
    "|": Pipe((Direction.North, Direction.South)),
    "-": Pipe((Direction.East, Direction.West)),
    "F": Pipe((Direction.South, Direction.East)),
    "7": Pipe((Direction.South, Direction.West)),
    "L": Pipe((Direction.North, Direction.East)),
    "J": Pipe((Direction.North, Direction.West)),
    ".": Pipe(None),
    "S": StartPipe(None),
}

OPP_DIRECTION: dict[Direction, Direction] = {
    Direction.North: Direction.South,
    Direction.East: Direction.West,
    Direction.West: Direction.East,
    Direction.South: Direction.North,
}


class PipeCoordinate(NamedTuple):
    pipe: Pipe
    coordinate: Coordinate


class PipeColumn(NamedTuple):
    pipe: Pipe
    column: int


type Data = list[list[Pipe]]
type GroupedLoop = dict[int, list[PipeColumn]]

data: Data


def parse_input(input: fileinput.FileInput[str]) -> Data:
    result = []
    for line in input:
        result.append([PIPETYPE[c] for c in line[:-1]])

    return result


def get_start_pos() -> Coordinate:
    for row, l in enumerate(data):
        for column, c in enumerate(l):
            if isinstance(c, StartPipe):
                return Coordinate(row, column)

    raise ValueError("StartPipe not found in data")


def get_next_direction(PipeCoordinate: Pipe, direction: Direction) -> Direction:
    if PipeCoordinate.ends is None:
        raise NonContinuousPipeError

    d1, d2 = PipeCoordinate.ends

    if OPP_DIRECTION[d1] == direction:
        return d2
    if OPP_DIRECTION[d2] == direction:
        return d1

    raise NonContinuousPipeError


def get_starting_pipe(end: Direction, start: Direction) -> Pipe:
    for pt in PIPETYPE.values():
        try:
            res = get_next_direction(pt, end)
        except NonContinuousPipeError:
            continue
        else:
            if res == start:
                return pt

            continue

    raise NonContinuousPipeError


def get_start_direction() -> Direction:
    start_pos = get_start_pos()

    for direction in Direction:
        next_row, next_column = get_next_pos(start_pos, direction)
        next = data[next_row][next_column]

        try:
            get_next_direction(next, direction)
        except NonContinuousPipeError:
            continue
        else:
            return direction

    raise NonContinuousPipeError


def group_coordinates(lc: list[PipeCoordinate]) -> GroupedLoop:
    gc = groupby(sorted(lc, key=lambda x: x.coordinate), lambda x: x.coordinate.row)
    return {k: [*(PipeColumn(p, c.column) for p, c in v)] for k, v in gc}


def make_row(ncl: list[PipeColumn]) -> list[Pipe]:
    res: list[Pipe] = [PIPETYPE["."] for _ in range(len(data[0]))]
    for p, c in ncl:
        res[c] = p

    return res


def area_row(ncl: list[PipeColumn]) -> int | NoReturn:
    vertical: int = 0
    corner: Pipe | None = None

    corners_vertical: dict[tuple[Pipe, Pipe], bool] = {
        (PIPETYPE["F"], PIPETYPE["7"]): False,
        (PIPETYPE["F"], PIPETYPE["J"]): True,
        (PIPETYPE["L"], PIPETYPE["J"]): False,
        (PIPETYPE["L"], PIPETYPE["7"]): True,
    }

    def isbounded(p: Pipe) -> bool:
        nonlocal vertical, corner

        if p == PIPETYPE["."]:
            return bool(vertical % 2)

        if p == PIPETYPE["|"]:
            vertical += 1

        if p in [PIPETYPE["7"], PIPETYPE["F"], PIPETYPE["J"], PIPETYPE["L"]]:
            if corner is None:
                corner = p

            else:
                vertical += corners_vertical[(corner, p)]
                corner = None

        return False

    row = make_row(ncl)
    res = [isbounded(p) for p in row]
    return res.count(True)


def area_loop(ln: list[PipeCoordinate]) -> int:
    area: int = 0

    for v in group_coordinates(ln).values():
        area += area_row(v)

    return area


def get_next_pos(pos: Coordinate, direction: Direction) -> Coordinate:
    start_row, start_column = pos

    match direction:
        case Direction.North:
            return Coordinate(start_row - 1, start_column)
        case Direction.South:
            return Coordinate(start_row + 1, start_column)
        case Direction.East:
            return Coordinate(start_row, start_column + 1)
        case Direction.West:
            return Coordinate(start_row, start_column - 1)


def trace_path(direction: Direction) -> list[PipeCoordinate]:
    curr_pos = get_next_pos(get_start_pos(), direction)
    start_direction = curr_direction = direction
    path: list[PipeCoordinate] = []

    while not isinstance((curr := data[curr_pos.row][curr_pos.column]), StartPipe):
        path.append(PipeCoordinate(curr, curr_pos))

        curr_direction = get_next_direction(curr, curr_direction)
        curr_pos = get_next_pos(curr_pos, curr_direction)

    path.append(
        PipeCoordinate(get_starting_pipe(curr_direction, start_direction), curr_pos)
    )
    return path


def main():
    global data

    with fileinput.input(encoding="utf-8") as file:
        data = parse_input(file)

    loop = trace_path(get_start_direction())
    P1 = ceil(len(loop) / 2)
    P2 = area_loop(loop)

    print(f"P1: {P1}")
    print(f"P2: {P2}")


if __name__ == "__main__":
    main()
