from __future__ import annotations

import fileinput
from enum import StrEnum
from functools import cache
from typing import NamedTuple


class Spring(StrEnum):
    Unknown = "?"
    Damaged = "#"
    Operational = "."


class Record(NamedTuple):
    springs: tuple[Spring, ...]
    counts: tuple[int, ...]

    def solve(self) -> int:
        return self._solve(self.springs, self.counts, False)

    @cache
    def _solve(
        self, springs: tuple[Spring, ...], counts: tuple[int, ...], active: bool
    ) -> int:
        if len(springs) == 0 and (len(counts) > 0 and counts != (0,)):
            return 0

        if len(springs) == 0 and (len(counts) == 0 or counts == (0,)):
            return 1

        new_counts: list[int] = list(counts)
        match springs[0]:

            case Spring.Unknown:
                r1 = self._solve(
                    (Spring.Damaged, *springs[1:]), tuple(new_counts), active
                )
                r2 = self._solve(
                    (Spring.Operational, *springs[1:]), tuple(new_counts), active
                )
                return r1 + r2

            case Spring.Operational:
                if active:
                    if new_counts[0] > 0:
                        return 0

                    if new_counts[0] == 0:
                        active = False
                        new_counts = new_counts[1:]
            case Spring.Damaged:
                if len(new_counts) == 0:
                    return 0

                if new_counts[0] == 0 and active:
                    return 0

                if new_counts[0] == 0 and not active:
                    print("wird thing happened")
                new_counts[0] -= 1
                active = True

        return self._solve(springs[1:], tuple(new_counts), active)


data: list[Record]


def expand_record(record: Record):
    return Record(
        springs=((*record.springs, Spring.Unknown) * 5)[:-1],
        counts=record.counts * 5,
    )


def parse_input(input: fileinput.FileInput[str]):
    res: list[Record] = []

    for line in input:
        springs_str, counts_str = line.split()
        res.append(
            Record(
                springs=tuple(Spring(c) for c in springs_str),
                counts=tuple(int(n) for n in counts_str.split(",")),
            )
        )

    return res


def main():
    global data

    with fileinput.input(encoding="utf-8") as input_file:
        data = parse_input(input_file)

    P1 = sum(r.solve() for r in data)
    P2 = sum(expand_record(r).solve() for r in data)

    print(f"P1: {P1}")
    print(f"P2: {P2}")


if __name__ == "__main__":
    main()
