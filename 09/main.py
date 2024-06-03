import fileinput
from collections.abc import Iterable
from itertools import pairwise

data: list[list[int]] = []


def parse_input(input_file: fileinput.FileInput[str]):
    for line in input_file:
        data.append([int(x) for x in line.split()])


def extrapolate(numbers: list[int]) -> int:
    result = 0
    curr = numbers

    while not all(n == 0 for n in curr):
        result += curr[-1]
        curr = [b - a for a, b in pairwise(curr)]

    return result


def main():
    with fileinput.input(encoding="utf-8") as input_file:
        parse_input(input_file)

    P1 = sum(extrapolate(n) for n in data)
    P2 = sum(extrapolate(n[::-1]) for n in data)

    print(f"P1: {P1}")
    print(f"P2: {P2}")


if __name__ == "__main__":
    main()
