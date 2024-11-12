import fileinput
from dataclasses import dataclass


@dataclass
class Assignments:
    first: tuple[int, int]
    second: tuple[int, int]

    def subsets(self) -> bool:
        s1 = set(range(self.first[0], self.first[1] + 1))
        s2 = set(range(self.second[0], self.second[1] + 1))

        return s2.issubset(s1) or s1.issubset(s2)

    def overlaps(self) -> bool:
        return (
            self.first[0] <= self.second[1] and self.first[1] >= self.second[0]
        ) or (self.second[0] <= self.first[1] and self.second[1] >= self.first[0])


def parse_assignment(ass: str) -> tuple[int, int]:
    nums = ass.split("-")
    return int(nums[0]), int(nums[1])


data: list[Assignments] = []
for line in fileinput.input():
    ass_1, ass_2 = line[:-1].split(",")
    data.append(Assignments(parse_assignment(ass_1), parse_assignment(ass_2)))


print(f"P1: {[a.subsets() for a in data].count(True)}")
print(f"P2: {[a.overlaps() for a in data].count(True)}")
