import fileinput
from collections.abc import Callable
from itertools import batched
from typing import NamedTuple


class MapLayout(NamedTuple):
    of: str
    to: str


class MapItem(NamedTuple):
    to_start: int
    of_start: int
    range_: int


class MapItemRange(NamedTuple):
    of_range: tuple[int, int]
    to_range: tuple[int, int]


type Range = tuple[int, int]

type MasterMap = list[list[MapItem]]
master_map: MasterMap = []


def sort_layer(layer: list[MapItem]) -> None:
    layer.sort(key=lambda mi: mi.of_start)


def calc_max(n: tuple[int, int]) -> int:
    min_, range_ = n
    return min_ + range_ - 1


def mi_range(mi: MapItem) -> MapItemRange:
    mir: Callable[[int], tuple[int, int]] = lambda n: (n, calc_max((n, mi.range_)))
    return MapItemRange(mir(mi.of_start), mir(mi.to_start))


def mi_next_value(v: int, mi: MapItem) -> int | None:
    mi_of_min, mi_of_max = mi_range(mi).of_range
    if mi_of_min <= v <= mi_of_max:
        mi_to_min, _mi_to_max = mi_range(mi).to_range
        return mi_to_min + (v - mi_of_min)
    return None


def mil_next_value(v: int, next_map: list[MapItem]) -> int:
    for mi in next_map:
        if (r := mi_next_value(v, mi)) is not None:
            return r
    return v


def solve_detached(seed: int):
    s = seed
    for next_mapping in master_map:
        s = mil_next_value(s, next_mapping)

    return s


def _mi_next_range(pr: Range, mi: MapItem) -> Range:
    p_min, p_max = pr
    mi_of_min, mi_of_max = mi_range(mi).of_range

    if (n_min := mi_next_value(p_min, mi)) is not None and (
        n_max := mi_next_value(p_max, mi)
    ) is not None:
        return n_min, n_max
    else:
        raise Exception("mi_next_value returned None.")


def _mil_next_ranges(p: Range, mil: list[MapItem]) -> list[Range]:
    p_min, p_max = p
    result: list[tuple[int, int]] = []

    for mi in mil:
        mi_of_min, mi_of_max = mi_range(mi).of_range

        if mi_of_min > p_max:
            break

        if (c_min := max(p_min, mi_of_min)) < (c_max := min(p_max, mi_of_max)):
            if c_min > p_min:
                result.append((p_min, c_min - 1))

            result.append(_mi_next_range((c_min, c_max), mi))
            p_min = c_max + 1

    if p_min < p_max:
        result.append((p_min, p_max))

    return result


def solve_range(rl: list[Range]) -> list[Range]:
    curr_ranges: list[Range] = rl
    next_ranges: list[Range] = []

    for i, layer in enumerate(master_map):
        for r in curr_ranges:
            next_ranges.extend(_mil_next_ranges(r, layer))
        curr_ranges = next_ranges
        next_ranges = []

    return curr_ranges


with fileinput.input(encoding="utf-8") as input_file:
    seeds = [int(s) for s in next(input_file)[7:].split()]

    for l in input_file:
        if len(l) <= 1:
            continue

        if l[-2] == ":":
            if len(master_map) > 0:
                sort_layer(master_map[-1])

            master_map.append([])
            continue

        master_map[-1].append(MapItem(*(int(n) for n in l.split())))

    sort_layer(master_map[-1])

p1_sol = min(solve_detached(s) for s in seeds)

seeds_ranged = ((low, calc_max((low, range_))) for low, range_ in batched(seeds, 2))
seeds_ranged_result: list[int] = []
seeds_ranged_result.append(min(r[0] for r in solve_range([*seeds_ranged])))
p2_sol = min(seeds_ranged_result)

print(f"P1: {p1_sol}")
print(f"P2: {p2_sol}")
