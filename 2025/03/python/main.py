import fileinput
from itertools import dropwhile


class Battery(list[int]):
    def __init__(self, qty):
        super().__init__(0 for _ in range(qty))

    def joltage(self) -> int:
        res: int = 0
        for j in self:
            res = res * 10 + j

        return res


class Bank(list[int]):
    def __init__(self, line: str):
        super().__init__([int(c) for c in line])

    def max_joltage(self, qty: int) -> int:
        battery: Battery = Battery(qty)
        for c in self:
            if battery[-1] != 0:
                for i in dropwhile(
                    lambda x: battery[x + 1] <= battery[x], range(len(battery) - 1)
                ):
                    battery[i] = battery[i + 1]
                    battery[i + 1] = 0

            if c > battery[-1]:
                battery[-1] = c

        return battery.joltage()


type Data = list[Bank]


def parse() -> Data:
    res: Data = []
    for line in fileinput.input():
        res.append(Bank(line[:-1]))

    return res


if __name__ == "__main__":
    data = parse()
    print(f"P1: {sum(bank.max_joltage(2) for bank in data)}")
    print(f"P2: {sum(bank.max_joltage(12) for bank in data)}")
