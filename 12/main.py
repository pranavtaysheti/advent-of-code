import fileinput
from enum import StrEnum
from typing import NamedTuple


class Spring(StrEnum):
    Unknown = "?"
    Damaged = "#"
    Operational = "."


class Record(NamedTuple):
    springs: list[Spring]
    counts: list[int]


data: list[Record]


def parse_input(input: fileinput.FileInput[str]):
    res: list[Record] = []

    for line in input:
        springs_str, counts_str = line.split()
        res.append(
            Record(
                springs=[Spring(c) for c in springs_str],
                counts=[int(n) for n in counts_str.split(",")],
            )
        )

    return res


def main():
    global data

    with fileinput.input(encoding="utf-8") as input_file:
        data = parse_input(input_file)

    print(data)


if __name__ == "__main__":
    main()
