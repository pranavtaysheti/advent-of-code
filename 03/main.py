from __future__ import annotations
from collections.abc import Generator
from itertools import takewhile, dropwhile, chain
from typing import Never, NamedTuple

INPUT_FILE = "input.txt"
INPUT_WIDTH = 140
FILLER_CHAR = "."
BUFFER_LINE = [FILLER_CHAR] * 140
GEAR_CHAR = "*"


class FoundDigit(NamedTuple):
    pos: int
    digit: str


def calculate_num(l: list[str]) -> int:
    return int("".join(l))


def get_surrounding_chars(b: int, e: int, sec: list[list[str]]) -> list[str]:
    return [
        *sec[0][b - 1 : e + 2],
        sec[1][b - 1],
        sec[1][e + 1],
        *sec[2][b - 1 : e + 2],
    ]


def check_num(s: list[str]) -> bool:
    return any([False if c == "." else True for c in s])


def get_num(s: list[str]) -> Generator[list[FoundDigit], Never, None]:
    curr = [*enumerate(s)]

    def check_decimal(item: tuple[int, str]):
        i, c = item
        return c.isdecimal()

    while len(curr) > 0:
        curr = [*dropwhile(lambda e: not check_decimal(e), curr)]
        nums = [*takewhile(check_decimal, curr)]
        yield [FoundDigit(*n) for n in nums]
        curr = curr[len(nums) :]


p1_sum = 0
p2_sum = 0

with open(INPUT_FILE, "r") as file:
    input: list[list[str]] = [
        BUFFER_LINE,
        *[[FILLER_CHAR, *[c for c in l[0:-1]], FILLER_CHAR] for l in file],
        BUFFER_LINE,
    ]

for l, s in enumerate((input[i - 1 : i + 2] for i in range(1, len(input) - 1))):
    nums_s = [[*get_num(s[i])] for i in range(3)]

    # P1
    for n in nums_s[1]:
        if len(n) == 0:
            continue

        pos = [e.pos for e in n]
        digits = [e.digit for e in n]

        b, e = pos[0], pos[-1]

        if check_num(get_surrounding_chars(b, e, s)):
            p1_sum += calculate_num(digits)

    # P2
    gears_pos = [p for p, c in enumerate(s[1]) if c == GEAR_CHAR]
    for gear_pos in gears_pos:
        nums_flat = chain.from_iterable(nums_s)
        surr_nums: list[int] = []
        surr_num_pos = [p for p in range(gear_pos - 1, gear_pos + 2)]

        for num in nums_flat:
            pos = [n.pos for n in num]
            digits = [n.digit for n in num]

            for p in pos:
                if p in surr_num_pos:
                    surr_nums.append(calculate_num(digits))
                    break

        if len(surr_nums) == 2:
            p2_sum += surr_nums[0] * surr_nums[1]

print(f"P1: {p1_sum}")
print(f"P2: {p2_sum}")
