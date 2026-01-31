import fileinput
from collections import deque
from collections.abc import Iterable
from enum import IntEnum, auto
from itertools import combinations, pairwise, product
from typing import NamedTuple


class Tile(IntEnum):
    NONE = auto()
    RED = auto()
    GREEN = auto()


class Point(NamedTuple):
    x: int
    y: int


def area(p1: Point, p2: Point):
    diff_x = abs(p1.x - p2.x) + 1
    diff_y = abs(p1.y - p2.y) + 1

    return diff_x * diff_y


class Data:
    _data: list[Point]
    _is_processed: bool
    _comp_region: list[list[Tile]]
    _flood_region: list[list[bool]]
    _prefix_sum: list[list[int]]
    _comp_x: dict[int, int]
    _comp_y: dict[int, int]

    def __init__(self, data: Iterable[Point]) -> None:
        self._data = [*data]
        self._is_processed = False

    def _compress(self):
        self._comp_x: dict[int, int] = {}
        curr = 1
        for cx in sorted({p.x for p in self._data}):
            self._comp_x[cx] = curr
            curr += 2

        self._comp_y: dict[int, int] = {}
        curr = 1
        for cy in sorted({p.y for p in self._data}):
            self._comp_y[cy] = curr
            curr += 2

        w, h = len(self._comp_x) * 2 + 1, len(self._comp_y) * 2 + 1
        self._comp_region = [[Tile.NONE] * w for _ in range(h)]

    def _connect(self):
        def connect(p1: Point, p2: Point):
            p1_comp = Point(self._comp_x[p1.x], self._comp_y[p1.y])
            p2_comp = Point(self._comp_x[p2.x], self._comp_y[p2.y])

            min_x, max_x = min(p1_comp.x, p2_comp.x), max(p1_comp.x, p2_comp.x)
            min_y, max_y = min(p1_comp.y, p2_comp.y), max(p1_comp.y, p2_comp.y)
            for ix, iy in product(
                range(min_x, max_x + 1),
                range(min_y, max_y + 1),
            ):
                self._comp_region[iy][ix] = Tile.GREEN

            self._comp_region[p1_comp.y][p1_comp.x] = Tile.RED
            self._comp_region[p2_comp.y][p2_comp.x] = Tile.RED

        for p1, p2 in pairwise(self._data):
            connect(p1, p2)
        connect(self._data[-1], self._data[0])

    def _flood_outside(self):
        w, h = len(self._comp_region[0]), len(self._comp_region)

        self._flood_region = [[False] * w for _ in range(h)]
        self._flood_region[0][0] = True
        queue: deque[tuple[int, int]] = deque([(0, 0)])
        while queue:
            cy, cx = queue.popleft()
            for dy, dx in [(+1, 0), (-1, 0), (0, +1), (0, -1)]:
                ny, nx = cy + dy, cx + dx
                if (
                    0 <= ny < h
                    and 0 <= nx < w
                    and not self._flood_region[ny][nx]
                    and self._comp_region[ny][nx] == Tile.NONE
                ):
                    queue.append((ny, nx))
                    self._flood_region[ny][nx] = True

    def _build_prefix_sum(self):
        w, h = len(self._comp_region[0]), len(self._comp_region)

        self._prefix_sum = [[0] * (w + 1) for _ in range(h + 1)]
        for y in range(h):
            for x in range(w):
                self._prefix_sum[y + 1][x + 1] = (
                    self._flood_region[y][x]
                    + self._prefix_sum[y][x + 1]
                    + self._prefix_sum[y + 1][x]
                    - self._prefix_sum[y][x]
                )

    def _process(self):
        if self._is_processed:
            return

        self._compress()
        self._connect()
        self._flood_outside()
        self._build_prefix_sum()

        self._is_processed = True

    def _check(self, p1: Point, p2: Point) -> bool:
        assert self._is_processed

        min_y, max_y = min(p1.y, p2.y), max(p1.y, p2.y)
        y1, y2 = self._comp_y[min_y], self._comp_y[max_y]

        min_x, max_x = min(p1.x, p2.x), max(p1.x, p2.x)
        x1, x2 = self._comp_x[min_x], self._comp_x[max_x]

        diff = (
            self._prefix_sum[y2 + 1][x2 + 1]
            - self._prefix_sum[y2 + 1][x1]
            - self._prefix_sum[y1][x2 + 1]
            + self._prefix_sum[y1][x1]
        )

        return diff == 0

    def max_area(self) -> int:
        return max(area(p1, p2) for p1, p2 in combinations(self._data, 2))

    def max_area_inside(self) -> int:
        self._process()

        return max(
            area(p1, p2)
            for p1, p2 in combinations(self._data, 2)
            if self._check(p1, p2)
        )


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
    print(f"P2: {data.max_area_inside()}")
