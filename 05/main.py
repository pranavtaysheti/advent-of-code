from typing import NamedTuple
from itertools import pairwise
from collections.abc import Iterable, Callable
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


def mi_range(mi: MapItem) -> MapItemRange:
    max_: Callable[[int], int] = lambda n: n + mi.range_ - 1
    mir: Callable[[int], tuple[int, int]] = lambda n: (n, max_(n))
    return MapItemRange(mir(mi.of_start), mir(mi.to_start))


def is_maptitle(s: str) -> bool:
    return True if s[-2] == ":" else False


def parse_maplayout(s: str) -> MapLayout:
    r, _postfix = s.split()
    of, _a, to = r.split("-")
    return MapLayout(of, to)


def parse_mapitem(s: str) -> MapItem:
    return MapItem(*(int(n) for n in s.split()))


def get_next_value(v: int, next_map: list[MapItem]) -> int:
    for k in next_map:
        k_of_min, k_of_max = mi_range(k).of_range
        if k_of_min <= v <= k_of_max:
            k_to_min, _k_to_max = mi_range(k).to_range
            return k_to_min + (v - k_of_min)

    return v


def solve_map(m: list[list[MapItem]], seed: int):
    s = seed
    for next_mapping in m:
        s = get_next_value(s, next_mapping)

    return s


def common_range(p: MapItem, n: MapItem) -> tuple[int, int] | None:
    p_min, p_max = mi_range(p).of_range
    n_min, n_max = mi_range(n).to_range

    if (c_min := max(p_min, n_min)) < (c_max := min(p_max, n_max)):
        return c_min, c_max

    return None


def next_mapitems(pn: MapItem, nl: list[MapItem]) -> list[MapItem]:
    result: list[MapItem] = []

    for mi in nl:
        if common_range(pn, mi):
            result.append(mi)

    pprint(f"NEXT_MIS: {result}")
    return result


master_map: list[list[MapItem]] = []

with open("input.txt", "r") as input_file:
    seeds = [int(s) for s in next(input_file)[7:].split()]

    for l in input_file:
        if len(l) <= 1:
            continue

        if is_maptitle(l):
            master_map.append([])
            continue

        master_map[-1].append(parse_mapitem(l))

p1_sol = min((solve_map(master_map, s) for s in seeds))
p2_sol = 0

print(f"P1: {p1_sol}")
print(f"P2: {p2_sol}")
