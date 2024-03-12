from typing import NamedTuple
from itertools import batched
from collections.abc import Callable
from pprint import pprint


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
_master_map: MasterMap = []


def add_layer_mastermap() -> None:
    _master_map.append([])

    if len(_master_map) == 1:
        return

    _master_map[-2].sort(key=lambda mi: mi.of_start)


def add_item_mastermap(mil: MapItem):
    _master_map[-1].append(mil)


def get_mastermap() -> MasterMap:
    return _master_map


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
    for next_mapping in get_mastermap():
        s = mil_next_value(s, next_mapping)

    return s


def mi_next_range(pr: Range, mi: MapItem) -> Range:
    p_min, p_max = pr
    mi_of_min, mi_of_max = mi_range(mi).of_range
    c_min, c_max = max(p_min, mi_of_min), min(p_max, mi_of_max)

    if (n_min := mi_next_value(c_min, mi)) is not None and (
        n_max := mi_next_value(c_max, mi)
    ) is not None:
        return n_min, n_max
    else:
        raise Exception("mi_next_value returned None. Should not happen!!")


def _mil_next_ranges(p: Range, mil: list[MapItem]) -> list[Range]:
    p_min, p_max = p
    result: list[tuple[int, int]] = []

    for mi in mil:
        mi_of_min, mi_of_max = mi_range(mi).of_range

        if mi_of_min > p_max:  # PROBLEM
            break

        if (c_min := max(p_min, mi_of_min)) < (c_max := min(p_max, mi_of_max)):
            if c_min > p_min:
                result.append((p_min, c_min - 1))
            if (n_range := mi_next_range((c_min, c_max), mi)) is not None:
                result.append(n_range)
            else:
                raise Exception("RETURNED NONE! should not happen!!!")
            p_min = c_max + 1

    if p_min < p_max:
        result.append((p_min, p_max))

    return result


def solve_range(n: Range) -> list[Range]:
    curr_ranges: list[Range] = [n]
    next_ranges: list[Range] = []

    for i, layer in enumerate(get_mastermap()):
        for r in curr_ranges:
            next_ranges.extend(_mil_next_ranges(r, layer))
        curr_ranges = next_ranges
        next_ranges = []

    return curr_ranges


if __name__ == "__main__":
    with open("input.txt", "r") as input_file:
        seeds = [int(s) for s in next(input_file)[7:].split()]

        for l in input_file:
            if len(l) <= 1:
                continue

            if l[-2] == ":":
                add_layer_mastermap()
                continue

            add_item_mastermap(MapItem(*(int(n) for n in l.split())))

    add_layer_mastermap()
    get_mastermap().pop()

    p1_sol = min(solve_detached(s) for s in seeds)

    seeds_ranged = ((low, calc_max((low, range_))) for low, range_ in batched(seeds, 2))
    seeds_ranged_result: list[int] = []
    for seed_low, seed_high in seeds_ranged:
        seeds_ranged_result.append(
            min(r[0] for r in solve_range((seed_low, seed_high)))
        )
    p2_sol = min(seeds_ranged_result)

    print(f"P1: {p1_sol}")
    print(f"P2: {p2_sol}")
