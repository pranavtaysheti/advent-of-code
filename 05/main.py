from typing import NamedTuple
from itertools import pairwise
from collections.abc import Iterable


class MapLayout(NamedTuple):  # Needs to be hashable.
    of: str
    to: str


class MapItem(NamedTuple):
    to_start: int
    of_start: int
    length: int


def is_maptitle(s: str) -> bool:
    return True if s[-2] == ":" else False


def parse_maplayout(s: str) -> MapLayout:
    r, _postfix = s.split()
    of, _a, to = r.split("-")
    return MapLayout(of, to)


def parse_mapitem(s: str) -> MapItem:
    return MapItem(*(int(n) for n in s.split()))


def get_mapping(of: str) -> tuple[str, list[MapItem]] | None:
    for key, value in master_map.items():
        if key.of == of:
            return key.to, value

    return None


def get_next_value(v: int, next_map: list[MapItem]) -> int:
    for k in next_map:
        if k.of_start <= v < k.of_start + k.length:
            return k.to_start + (v - k.of_start)

    return v


def solve_map(seeds: Iterable[int]):
    result: list[int] = []

    for s in seeds:
        curr_name = "seed"
        while next_mapping := get_mapping(curr_name):
            curr_name, to_items = next_mapping
            s = get_next_value(s, to_items)

        result.append(s)

    return result


master_map: dict[MapLayout, list[MapItem]] = {}

with open("input.txt", "r") as input_file:
    seeds = [int(s) for s in next(input_file)[7:].split()]
    seeds_paired = pairwise(seeds)

    for l in input_file:
        if len(l) <= 1:
            continue

        if is_maptitle(l):
            curr_maplayout = parse_maplayout(l)
            master_map[curr_maplayout] = []
            continue

        master_map[curr_maplayout].append(parse_mapitem(l))  # type: ignore


p1_sol = min(solve_map(seeds))
p2_sol = 0

print(f"P1: {p1_sol}")
print(f"P2: {p2_sol}")
