from __future__ import annotations

import fileinput
from enum import StrEnum
from itertools import cycle
from turtle import right
from typing import NamedTuple

instructions: list[Direction] = []
network: dict[str, NodeNavigation] = {}

P1: int = 0
P2: int = 0


class Direction(StrEnum):
    RIGHT = "R"
    LEFT = "L"


class NodeNavigation(NamedTuple):
    left: str
    right: str


def parse_input(input_file: fileinput.FileInput[str]):
    global instructions, network

    instructions = [Direction(c) for c in input_file.readline()[:-1]]

    for line in input_file:
        if len(line) <= 1:
            continue

        node, left, right = line[0:3], line[7:10], line[12:15]
        network[node] = NodeNavigation(left, right)


def navigate(init: str, end: str) -> int:
    count: int = 0
    next = init

    for step in cycle(instructions):
        count += 1

        match step:
            case Direction.LEFT:
                next = network[next].left
            case Direction.RIGHT:
                next = network[next].right

        if next == end:
            break

    return count


def main():
    global P1, P2

    with fileinput.input(encoding="utf-8") as input_file:
        parse_input(input_file)

    P1 = navigate("AAA", "ZZZ")

    print(f"P1: {P1}")
    print(f"P2: {P2}")


if __name__ == "__main__":
    main()
