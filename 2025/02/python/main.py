import fileinput
from typing import NamedTuple, Self


class IDRange(NamedTuple):
    start: int
    end: int

    def seperate(self) -> tuple[list[Self], int]:
        res: list[Self] = []

        min_digits, max_digits = len(str(self.start)), len(str(self.end))
        curr = self.start
        for digits in range(min_digits, max_digits + 1):
            res.append(type(self)(curr, min(10**digits - 1, self.end)))
            curr = 10**digits

        return res, min_digits

    def fake_ids(self) -> set[int]:
        res: set[int] = set()

        def do_subrange(look_len: int):
            r_min, r_max = int(str(n1)[:look_len]), int(str(n2)[:look_len])
            for e in range(r_min, r_max + 1):
                if n1 <= (c_id := int(str(e) * (curr_len // look_len))) <= n2:
                    res.add(c_id)

        parts, min_len = self.seperate()
        for curr_len, (n1, n2) in enumerate(parts, min_len):
            if curr_len % 2 != 0:
                continue

            do_subrange(curr_len // 2)
            curr_len += 1

        print(res)
        return res


# def prime_factors(num: int) -> list[int]:
#     res: list[int] = []

#     if num % 2 == 0:
#         res.append(2)
#         while num % 2 == 0:
#             num //= 2

#     i = 3
#     while i * i <= num:
#         if num % i == 0:
#             res.append(i)
#             while num % i == 0:
#                 num //= i
#             i += 2

#     if num > 1:
#         res.append(i)

#     return res


def parse() -> list[IDRange]:
    pairs = fileinput.input().readline()[:-1].split(",")
    return [IDRange(int(n1), int(n2)) for p in pairs for n1, n2 in [p.split("-")]]


if __name__ == "__main__":
    data = parse()
    print(f"P1: {sum(id for idr in data for id in idr.fake_ids())}")
