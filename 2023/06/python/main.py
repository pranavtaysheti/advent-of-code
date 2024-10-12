import fileinput
from fileinput import FileInput
from math import ceil, floor, prod, sqrt
from typing import NamedTuple


class Race(NamedTuple):
    time: int
    distance: int


def parse_input(file: FileInput[str]) -> list[Race]:
    races: list[int] = [int(n) for n in file.readline()[9:].split()]
    distances: list[int] = [int(n) for n in file.readline()[9:].split()]

    return [Race(races[i], distances[i]) for i in range(len(races))]


def winning_ways(race: Race) -> int:
    discriminant = sqrt(pow(race.time, 2) - 4 * (race.distance + 1))
    high = floor((race.time + discriminant) / 2)
    low = ceil((race.time - discriminant) / 2)

    return high - low + 1


def main():
    data = parse_input(fileinput.input())

    P1 = prod(winning_ways(r) for r in data)
    P2 = winning_ways(
        Race(
            time=int("".join(str(r.time) for r in data)),
            distance=int("".join(str(r.distance) for r in data)),
        )
    )

    print(f"P1: {P1}")
    print(f"P2: {P2}")


if __name__ == "__main__":
    main()
