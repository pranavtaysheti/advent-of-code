import fileinput
from collections import UserList
from typing import Iterable


class Room(UserList[list[str]]):
    def __init__(self, inp: Iterable[str]):
        self.curr = 0
        data = [[c for c in l] for l in inp]
        for i, c in enumerate(data[0]):
            if c == "S":
                data[0][i] = "|"
                break

        super().__init__(data)

    def process_line(self):
        splits: int = 0
        for i, (prev, curr) in enumerate(
            zip(self.data[self.curr], self.data[self.curr + 1])
        ):
            if prev != "|":
                continue

            if curr == "^":
                if i > 0:
                    self.data[self.curr + 1][i + 1] = "|"
                if i < len(self.data[self.curr + 1]) - 1:
                    self.data[self.curr + 1][i - 1] = "|"

                splits += 1

            else:
                self.data[self.curr + 1][i] = "|"

        self.curr += 1
        return splits

    def process(self) -> list[int]:
        return [self.process_line() for _ in range(len(self.data) - 1)]


def parse() -> Room:
    return Room([l[:-1] for l in fileinput.input()])


if __name__ == "__main__":
    data = parse()
    print(f"P1: {sum(i for i in data.process())}")
