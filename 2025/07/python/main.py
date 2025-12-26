import fileinput
from typing import Iterable, Literal

type Cell = Literal["^"] | int


class Room:
    def __init__(self, inp: Iterable[str]):
        self.curr = 0
        self.splits: list[int] | None = None
        self.is_processed = False

        def rep(c) -> Cell:
            match c:
                case "^":
                    return c
                case ".":
                    return 0
                case "S":
                    return 1

            assert False, "Input data has errors"

        data: list[list[Cell]] = [[rep(c) for c in l] for l in inp]
        self._data = data

    def process_line(self):
        splits: int = 0
        for i, (prev, curr) in enumerate(
            zip(self._data[self.curr], self._data[self.curr + 1])
        ):
            if not isinstance(prev, int):
                continue

            next_row = self._data[self.curr + 1]

            if curr == "^":
                if i > 0:
                    n_cell = next_row[i + 1]
                    assert isinstance(n_cell, int)

                    next_row[i + 1] = n_cell + prev
                if i < len(self._data[self.curr + 1]) - 1:
                    n_cell = next_row[i - 1]
                    assert isinstance(n_cell, int)

                    next_row[i - 1] = n_cell + prev

                splits += 1

            else:
                n_cell = next_row[i]
                assert isinstance(n_cell, int)

                next_row[i] = n_cell + prev

        self.curr += 1
        return splits

    def process(self):
        if self.is_processed:
            return

        self.splits = [self.process_line() for _ in range(len(self._data) - 1)]
        self.is_processed = True

    def count_timelines(self):
        self.process()

        res: int = 0
        for c in self._data[-1]:
            assert isinstance(c, int)
            res += c

        return res


def parse() -> Room:
    return Room([l[:-1] for l in fileinput.input()])


if __name__ == "__main__":
    data = parse()
    data.process()

    assert data.splits is not None
    print(f"P1: {sum(i for i in data.splits)}")

    print(f"P2: {data.count_timelines()}")
