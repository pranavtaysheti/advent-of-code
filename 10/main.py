import fileinput
from enum import Enum, StrEnum, auto
from math import ceil
from typing import NamedTuple


class NonContinuousPipeError(Exception):
    pass


class Coordinate(NamedTuple):
    row: int
    column: int


class PipeType(StrEnum):
    Nothing = "."
    NorthSouth = "|"
    EastWest = "-"
    NorthEast = "L"
    NorthWest = "J"
    SouthEast = "F"
    SouthWest = "7"
    Starting = "S"


class Direction(Enum):
    North = auto()
    South = auto()
    East = auto()
    West = auto()


data: list[list[PipeType]] = []
step_count: dict[Direction, int]


def parse_input(input: fileinput.FileInput[str]):
    for line in input:
        data.append([PipeType(c) for c in line[:-1]])


def get_start_pos() -> Coordinate:
    for row, l in enumerate(data):
        for column, c in enumerate(l):
            if c == PipeType.Starting:
                return Coordinate(row, column)

    raise AssertionError("PipeType.Starting not found in data")


def get_next_direction(node: PipeType, direction: Direction) -> Direction:

    match (node, direction):
        case (PipeType.EastWest, Direction.West | Direction.East):
            return direction
        case (PipeType.NorthSouth, Direction.North | Direction.South):
            return direction
        case (PipeType.NorthEast, Direction.South):
            return Direction.East
        case (PipeType.NorthEast, Direction.West):
            return Direction.North
        case (PipeType.NorthWest, Direction.East):
            return Direction.North
        case (PipeType.NorthWest, Direction.South):
            return Direction.West
        case (PipeType.SouthEast, Direction.North):
            return Direction.East
        case (PipeType.SouthEast, Direction.West):
            return Direction.South
        case (PipeType.SouthWest, Direction.North):
            return Direction.West
        case (PipeType.SouthWest, Direction.East):
            return Direction.South
        case _:
            raise NonContinuousPipeError


def get_start_direction() -> Direction | None:
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

    return None


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


def trace_path(direction: Direction) -> int:
    curr_pos = get_next_pos(get_start_pos(), direction)
    curr_direction = direction
    count: int = 0

    while (curr := data[curr_pos.row][curr_pos.column]) != PipeType.Starting:
        if curr == PipeType.Nothing:
            raise NonContinuousPipeError

        try:
            curr_direction = get_next_direction(curr, curr_direction)
        except NonContinuousPipeError:
            print(curr)
            print(curr_direction)
            print(count)
            raise
        else:
            curr_pos = get_next_pos(curr_pos, curr_direction)
            count += 1

    return count


def main():
    with fileinput.input(encoding="utf-8") as file:
        parse_input(file)

    P1 = ceil(trace_path(Direction.East) / 2)
    P2 = 0

    print(f"P1: {P1}")
    print(f"P2: {P2}")


if __name__ == "__main__":
    main()
