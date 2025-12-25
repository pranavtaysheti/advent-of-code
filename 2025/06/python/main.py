import fileinput
from math import prod
from typing import NamedTuple


class Problem(NamedTuple):
    nums: list[int]
    operator: str

    def solve(self) -> int:
        match self.operator:
            case "*":
                return prod(self.nums)
            case "+":
                return sum(n for n in self.nums)

        raise AssertionError("Input is incorrect")


def scan_input() -> list[str]:
    return [l[:-1] for l in fileinput.input()]


def parse1(raw_input: list[str]):
    num_lines: list[list[int]] = [
        [int(n) for n in raw_input[i].split()] for i in range(4)
    ]
    operator_line: list[str] = [o for o in raw_input[4].split()]

    return [Problem([*i[:-1]], i[-1]) for i in zip(*num_lines, operator_line)]


def parse2(ri: list[str]) -> list[Problem]:
    res: list[Problem] = []

    curr_nums: list[int] = []
    curr_oper: str = ""
    sub_no: int = 0
    for i in range(max(len(ri[0]), len(ri[1]), len(ri[2]), len(ri[3]))):
        col = "".join([ri[y][i] for y in range(len(ri))])

        if all([(lambda x: x == " ")(c) for c in col]):
            res.append(Problem(curr_nums, curr_oper))
            curr_nums, curr_oper = [], ""
            sub_no = 0
            continue

        curr_nums.append(int(col[:-1]))
        if sub_no == 0:
            curr_oper = col[-1]

        sub_no += 1

    res.append(Problem(curr_nums, curr_oper))
    return res


if __name__ == "__main__":
    raw_input = scan_input()

    data1 = parse1(raw_input)
    print(f"P1: {sum(s.solve() for s in data1)}")

    data2 = parse2(raw_input)
    print(f"P2: {sum(s.solve() for s in data2)}")
