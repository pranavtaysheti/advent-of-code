import fileinput
from collections import Counter
from collections.abc import Iterator
from enum import Enum, StrEnum, auto
from typing import Iterable

TOTAL_CYCLES = 1_000_000_000


class Rock(StrEnum):
    EMPTY_SPACE = "."
    ROUND = "O"
    CUBE = "#"


class Direction(Enum):
    NORTH = auto()
    WEST = auto()
    SOUTH = auto()
    EAST = auto()


type Data = list[list[Rock]]
data: Data


def parse_input(input: fileinput.FileInput[str]) -> Data:
    res = []
    for line in input:
        res.append([Rock(c) for c in line[:-1]])

    return res


def data_iter(direction: Direction) -> Iterator[list[Rock]]:
    column_range = range(len(data[0]))

    def columns_iter(num_iter: Iterable[int]):
        return ([row[col] for row in data] for col in num_iter)

    match direction:
        case Direction.NORTH:
            return columns_iter(column_range)
        case Direction.WEST:
            return iter(data)
        case Direction.SOUTH:
            return columns_iter(reversed(column_range))
        case Direction.EAST:
            return reversed(data)


def spin(data: Data) -> Data: ...


def roll_north(line: list[Rock]) -> list[int]:
    def contains_round(low: int, high: int) -> int:
        return Counter(line[low + 1 : high])[Rock.ROUND]

    def roll(low: int, high: int) -> list[int]:
        count = contains_round(low, high)
        return [low + 1 + i for i in range(count)]

    cubes_pos = [i for i, r in enumerate(line) if r == Rock.CUBE]

    res: list[int] = []
    curr = -1

    for pos in cubes_pos:
        res.extend(roll(curr, pos))
        curr = pos

    res.extend(roll(curr, len(line)))

    return res


def total_load(line: list[Rock]) -> int:
    return sum(len(data) - i for i in roll_north(line))


def main():
    global data

    with fileinput.input(encoding="utf8") as file_input:
        data = parse_input(file_input)

    P1: int = sum(total_load(l) for l in data_iter(Direction.NORTH))
    P2: int = 0

    print(f"P1: {P1}")
    print(f"P2: {P2}")


if __name__ == "__main__":
    main()
