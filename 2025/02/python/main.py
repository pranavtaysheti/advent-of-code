import fileinput
from collections.abc import Callable
from math import log10
from typing import NamedTuple, Self


class IDRange(NamedTuple):
    start: int
    end: int

    def seperate(self) -> tuple[list[Self], int]:
        res: list[Self] = []

        min_digits, max_digits = int(log10(self.start)) + 1, int(log10(self.end)) + 1
        curr = self.start
        for digits in range(min_digits, max_digits + 1):
            res.append(type(self)(curr, min(10**digits - 1, self.end)))
            curr = 10**digits

        return res, min_digits

    def fake_ids(self, look_len_selector: Callable[[int], list[int]]) -> set[int]:
        res: set[int] = set()

        parts, min_len = self.seperate()
        for curr_len, (n1, n2) in enumerate(parts, min_len):
            for look_len in look_len_selector(curr_len):
                r_min, r_max = int(str(n1)[:look_len]), int(str(n2)[:look_len])
                for e in range(r_min, r_max + 1):
                    if n1 <= (c_id := int(str(e) * (curr_len // look_len))) <= n2:
                        res.add(c_id)

            curr_len += 1

        return res


def prime_factors(num: int) -> list[int]:
    res: list[int] = []

    if num % 2 == 0:
        res.append(2)
        while num % 2 == 0:
            num //= 2

    i = 3
    while i * i <= num:
        if num % i == 0:
            res.append(i)
            while num % i == 0:
                num //= i
            i += 2

    if num > 1:
        res.append(num)

    return res


def parse() -> list[IDRange]:
    pairs = fileinput.input().readline().split(",")
    return [IDRange(int(n1), int(n2)) for p in pairs for n1, n2 in [p.split("-")]]


if __name__ == "__main__":
    data = parse()

    P1_selector = lambda l: [l // 2] if l % 2 == 0 else []
    print(f"P1: {sum(id for idr in data for id in idr.fake_ids(P1_selector))}")

    P2_selector = lambda l: [l // f for f in prime_factors(l)]
    print(f"P2: {sum(id for idr in data for id in idr.fake_ids(P2_selector))}")
