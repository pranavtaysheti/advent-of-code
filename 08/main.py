from __future__ import annotations

import fileinput
import math
import re
from collections import OrderedDict
from collections.abc import Iterable
from enum import StrEnum
from itertools import pairwise
from typing import NamedTuple


class NodeNavigation(NamedTuple):
    left: str
    right: str


class NavigatorResult(NamedTuple):
    end: str
    steps: int
    pos: int


class Direction(StrEnum):
    RIGHT = "R"
    LEFT = "L"


instructions: list[Direction] = []
network: OrderedDict[str, NodeNavigation] = OrderedDict()


def parse_input(input_file: fileinput.FileInput[str]):
    global instructions, network

    instructions = [Direction(c) for c in input_file.readline()[:-1]]

    for line in input_file:
        if len(line) <= 1:
            continue

        node, left, right = line[0:3], line[7:10], line[12:15]
        network[node] = NodeNavigation(left, right)


def navigate(init: str, end_pattern: str, instruction_pos: int = 0) -> NavigatorResult:
    steps: int = 0
    next = init
    curr: int = instruction_pos

    while re.search(end_pattern, next) is None:
        steps += 1

        match instructions[curr]:
            case Direction.LEFT:
                next = network[next].left
            case Direction.RIGHT:
                next = network[next].right

        curr = (curr + 1) % len(instructions)

    return NavigatorResult(next, steps, curr)


def navigate_thorough(init: str, end_pattern: str):
    steps_db: list[int] = []
    next = init
    end_pos = None

    while end_pos != 0:
        end, steps, end_pos = navigate(next, end_pattern)
        steps_db.append(steps)
        next = end

    return steps_db


def navigate_all(init_pattern: str, end_pattern: str) -> dict[str, list[int]]:
    routes: dict[str, list[int]] = {}

    for node in network:
        if re.search(init_pattern, node) is None:
            continue

        routes[node] = navigate_thorough(node, end_pattern)

    return routes


def lcm(numbers: Iterable[int]):
    return math.prod(numbers) // math.prod(
        [math.gcd(x, y) for x, y in pairwise(numbers)]
    )


def main():
    with fileinput.input(encoding="utf-8") as input_file:
        parse_input(input_file)

    _, P1, _ = navigate("AAA", "^ZZZ$")
    P2: int = lcm([sum(n) for n in navigate_all("A$", "Z$").values()])

    print(f"P1: {P1}")
    print(f"P2: {P2}")


if __name__ == "__main__":
    main()
