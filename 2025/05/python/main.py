import fileinput
from itertools import combinations
from typing import NamedTuple


class IDRange(NamedTuple):
    low: int
    high: int

    def length(self):
        return self.high - self.low + 1


class IDRanges(list[IDRange]):
    def check(self, num: int) -> bool:
        for low, high in self:
            if low <= num <= high:
                return True

        return False

    def sort_low(self):
        return sorted(self, key=lambda x: x.low * (10**62) + x.high)

    def merge_range(self) -> IDRanges:
        res = IDRanges()
        sorted_self = self.sort_low()

        vor = sorted_self[0]
        for nach in sorted_self[1:]:
            if nach.low > vor.high:
                res.append(vor)
                vor = nach
            else:
                vor = IDRange(vor.low, max(vor.high, nach.high))

        return IDRanges([*res, vor])


def parse() -> tuple[IDRanges, list[int]]:
    id_ranges = IDRanges()
    nums: list[int] = []
    fp_input = fileinput.input()

    for line in fp_input:
        if len(line) == 1:
            break

        [low, high] = [int(n) for n in line[:-1].split("-")]
        id_ranges.append(IDRange(low, high))

    for line in fp_input:
        nums.append(int(line[:-1]))

    return id_ranges, nums


if __name__ == "__main__":
    id_ranges, nums = parse()

    print(f"P1: {sum(id_ranges.check(num) for num in nums)}")
    print(f"P2: {sum(idr.length() for idr in id_ranges.merge_range())}")
