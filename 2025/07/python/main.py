import fileinput
from functools import cache
from typing import Iterable, Literal

type Cell = Literal["^"] | int


class Room:
    def __init__(self, inp: Iterable[str]):
        self.curr = 0

        def rep(c) -> Cell:
            match c:
                case "^":
                    return c
                case ".":
                    return 0
                case "S":
                    return 1

            raise AssertionError("Input Data has errors")

        data: list[list[Cell]] = [[rep(c) for c in l] for l in inp]
        self._data = data

    def process_line(self):
        splits: int = 0
        for i, (prev, curr) in enumerate(
            zip(self._data[self.curr], self._data[self.curr + 1])
        ):
            if not isinstance(prev, int):
                continue

            if curr == "^":
                if i > 0:
                    self._data[self.curr + 1][i + 1] += prev
                if i < len(self._data[self.curr + 1]) - 1:
                    self._data[self.curr + 1][i - 1] += prev

                splits += 1

            else:
                self._data[self.curr + 1][i] += prev

        self.curr += 1
        return splits

    @cache
    def process(self) -> list[int]:
        return [self.process_line() for _ in range(len(self._data) - 1)]

    def count_timelines(self):
        self.process()
        return sum(c for c in self._data[-1])


def parse() -> Room:
    return Room([l[:-1] for l in fileinput.input()])


if __name__ == "__main__":
    data = parse()
    print(f"P1: {sum(i for i in data.process())}")
    print(f"P2: {data.count_timelines()}")
