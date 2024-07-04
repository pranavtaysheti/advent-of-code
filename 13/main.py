import fileinput
from enum import Enum, StrEnum, auto
from functools import partial
from itertools import compress
from typing import NamedTuple


class Cell(StrEnum):
    ASH = "."
    ROCKS = "#"


class ReflectionType(Enum):
    ONEOFF = auto()
    PERFECT = auto()


class Coordinate(NamedTuple):
    row: int
    column: int


class Reflection(NamedTuple):
    type_: ReflectionType
    line: int


class TerrainData(NamedTuple):
    horizontal: list[Reflection]
    vertical: list[Reflection]


type Terrain = list[list[Cell]]
data: list[Terrain]


def parse_input(input_file: fileinput.FileInput[str]):
    data: list[Terrain] = []

    terrain: Terrain = []
    for line in input_file:
        if len(line) == 1:
            data.append(terrain)
            terrain = []
            continue

        terrain.append([Cell(c) for c in line[:-1]])

    data.append(terrain)
    return data


def summarize(terrain: Terrain, type_: ReflectionType) -> int:
    terrain_data = analyze(terrain)
    # print(terrain_data)
    res: int = 0

    def check(type_: ReflectionType, data: list[Reflection]) -> int:
        res = [*filter(lambda x: x.type_ == type_, data)]
        if len(res) == 1:
            return res[0].line

        return 0

    res += 100 * check(type_, terrain_data.horizontal)
    res += 1 * check(type_, terrain_data.vertical)
    return res


def analyze(terrain: Terrain) -> TerrainData:
    def transpose(terrain: Terrain) -> Terrain:
        return [[line[i] for line in terrain] for i in range(len(terrain[0]))]

    def diffs(r1: list[Cell], r2: list[Cell]) -> list[int]:
        selectors = [c1 != c2 for c1, c2 in zip(r1, r2)]
        return [*compress([i for i in range(len(r1))], selectors)]

    def reflection(terrain: Terrain, i: int) -> ReflectionType | None:
        left: Terrain = terrain[: i + 1]
        right: Terrain = terrain[i + 1 :]
        width = min(len(left), len(right))
        one_off: bool = False

        for j in range(width):
            if (m := left[-j - 1]) != (n := right[j]):
                diff_cells = diffs(m, n)
                if len(diff_cells) > 1 or one_off:
                    return None

                one_off = True

        if one_off:
            return ReflectionType.ONEOFF

        return ReflectionType.PERFECT

    def orientation(terrain: Terrain) -> list[Reflection]:
        res: list[Reflection] = []
        reflection_co = partial(reflection, terrain)
        for i in range(len(terrain) - 1):
            if (reflection_type := reflection_co(i)) is not None:
                res.append(Reflection(reflection_type, i + 1))

        return res

    return TerrainData(
        horizontal=orientation(terrain),
        vertical=orientation(transpose(terrain)),
    )


def main():
    global data

    with fileinput.input(encoding="utf-8") as input_file:
        data = parse_input(input_file)

    P1: int = sum(summarize(terrain, ReflectionType.PERFECT) for terrain in data)
    P2: int = sum(summarize(terrain, ReflectionType.ONEOFF) for terrain in data)

    print(f"P1: {P1}")
    print(f"P2: {P2}")


if __name__ == "__main__":
    main()
