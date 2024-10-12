import fileinput
from functools import cache
from itertools import combinations
from typing import NamedTuple


class Coordinate(NamedTuple):
    row: int
    column: int


class EmptyLines(NamedTuple):
    rows: set[int]
    columns: set[int]


type Data = list[list[bool]]
data: Data
galaxy_coordinates: list[Coordinate]
empty_space: EmptyLines


def get_galaxy_coordinates() -> list[Coordinate]:
    coordinates: list[Coordinate] = []
    for i, row in enumerate(data):
        for j, cell in enumerate(row):
            if cell:
                coordinates.append(Coordinate(i, j))

    return coordinates


def get_empty_space() -> EmptyLines:
    occ_rows: set[int] = set(r for r, _ in galaxy_coordinates)
    occ_columns: set[int] = set(c for _, c in galaxy_coordinates)

    all_rows = set(i for i in range(len(data)))
    all_columns = set(i for i in range(len(data[0])))
    return EmptyLines(all_rows - occ_rows, all_columns - occ_columns)


def count_steps(g1: Coordinate, g2: Coordinate, factor: int) -> int:
    res: int = 0

    def count_line(n1: int, n2: int, empty_points: set[int]):
        nonlocal res

        def empty_space_count() -> int:
            return len(set(range(lower + 1, upper)).intersection(empty_points))

        lower, upper = sorted([n1, n2])
        res += upper - lower
        res += empty_space_count() * (factor - 1)

    count_line(g1.row, g2.row, empty_space.rows)
    count_line(g1.column, g2.column, empty_space.columns)

    return res


def parse_input(input: fileinput.FileInput) -> Data:
    res: Data = []
    for line in input:
        res.append([True if c == "#" else False for c in line[:-1]])

    return res


def sum_steps(factor: int) -> int:
    pairs = combinations(galaxy_coordinates, 2)
    return sum(count_steps(g1, g2, factor) for g1, g2 in pairs)


def main():
    global data, galaxy_coordinates, empty_space

    with fileinput.input(encoding="utf-8") as input:
        data = parse_input(input)

    galaxy_coordinates = get_galaxy_coordinates()
    empty_space = get_empty_space()

    P1: int = sum_steps(2)
    P2: int = sum_steps(1_000_000)

    print(f"P1: {P1}")
    print(f"P2: {P2}")


if __name__ == "__main__":
    main()
