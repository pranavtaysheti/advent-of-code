import enum
import fileinput
from collections import Counter
from collections.abc import Iterator
from enum import StrEnum
from typing import Iterable, Literal, NamedTuple

type Direction = Literal["clockwise"] | Literal["anti-clockwise"]
type Data = list[list[Rock]]
type DataIter = Iterator[list[Rock]]


class Rock(StrEnum):
    EMPTY_SPACE = "."
    ROUND = "O"
    CUBE = "#"


def parse_input(input: fileinput.FileInput[str]) -> Data:
    res = []
    for line in input:
        res.append([Rock(c) for c in line[:-1]])

    return res


def rotate_anticlockwise(data: Data) -> Data:
    return [[row[col] for row in data] for col in reversed(range(len(data)))]


def rotate_clockwise(data: Data) -> Data:
    return [[row[col] for row in reversed(data)] for col in range(len(data))]


def tilt_platform(data_iter: Data) -> Data:
    def roll_line(line: list[Rock]) -> list[Rock]:
        res: list[Rock] = [Rock.EMPTY_SPACE for _ in range(len(line))]
        cubes_pos = [i for i, r in enumerate(line) if r == Rock.CUBE]

        def roll(low: int, high: int) -> list[int]:
            count = Counter(line[low + 1 : high])[Rock.ROUND]
            return [low + 1 + i for i in range(count)]

        def write_res(type_: Rock, pos: list[int]):
            for i in pos:
                res[i] = type_

        write_res(Rock.CUBE, cubes_pos)

        curr = -1
        for pos in cubes_pos:
            write_res(Rock.ROUND, roll(curr, pos))
            curr = pos

        write_res(Rock.ROUND, roll(curr, len(line)))
        return res

    return [roll_line(l) for l in data_iter]


def spin_n(reps: int) -> Data:
    class Solution(NamedTuple):
        non_loop: int
        loop_len: int

    cache: list[Data] = []

    def spin(data: Data) -> Data:
        res: Data = data

        for _ in range(4):
            res = tilt_platform(res)
            res = rotate_clockwise(res)

        return res

    def solve() -> Solution:
        curr = rotate_anticlockwise(data)

        def check() -> int | None:
            for i, d in enumerate(cache):
                if d == curr:
                    return i

        i: int = 0
        while (prev := check()) is None:
            cache.append(curr)
            curr = spin(curr)
            i += 1

        return Solution(prev, i - prev)

    non_loop, loop_len = solve()
    return cache[non_loop + (reps - non_loop) % loop_len]


def total_load(data: Data) -> int:
    def line_load(line: list[Rock]) -> int:
        loads = [len(data) - i for i, s in enumerate(line) if s == Rock.ROUND]
        return sum(loads)

    return sum(line_load(l) for l in data)


def main():
    global data
    TOTAL_CYCLES = 1_000_000_000

    with fileinput.input(encoding="utf8") as file_input:
        data = parse_input(file_input)

    P1: int = total_load(tilt_platform(rotate_anticlockwise(data)))
    P2: int = total_load(spin_n(TOTAL_CYCLES))

    print(f"P1: {P1}")
    print(f"P2: {P2}")


if __name__ == "__main__":
    main()
