import fileinput
from collections.abc import Iterable
from itertools import chain, combinations, product
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


def area(p1: Point, p2: Point):
    diff_x = abs(p1.x - p2.x) + 1
    diff_y = abs(p1.y - p2.y) + 1

    return diff_x * diff_y


class Data:
    _data: list[Point]

    def __init__(self, data: Iterable[Point]) -> None:
        self._data = [*data]

    def max_area(self) -> int:
        return max(area(p1, p2) for p1, p2 in combinations(self._data, 2))


def parse() -> Data:
    return Data(
        [
            Point(int(x), int(y))
            for l in fileinput.input()
            for x, y in [l[:-1].split(",")]
        ]
    )


if __name__ == "__main__":
    data = parse()

    print(f"P1: {data.max_area()}")
