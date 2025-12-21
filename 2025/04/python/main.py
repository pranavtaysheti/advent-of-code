import fileinput
from itertools import product

type pos = tuple[int, int]


class Room(list[list[bool]]):
    def count_around(self, row: int, col: int):
        rows, cols = [row], [col]
        if row != len(self) - 1:
            rows.append(row + 1)
        if row != 0:
            rows.append(row - 1)
        if col != len(self[row]) - 1:
            cols.append(col + 1)
        if col != 0:
            cols.append(col - 1)

        return sum(1 for row, col in product(rows, cols) if self[row][col] == True)

    def removables(self) -> list[pos]:
        res: list[pos] = []
        for row, col in product(range(len(self)), range(len(self[0]))):
            if self[row][col] == True:
                if data.count_around(row, col) < 5:
                    res.append((row, col))

        return res

    def cleanup(self) -> int:
        items = self.removables()
        for row, col in items:
            self[row][col] = False

        return len(items)


def parse() -> Room:
    res = Room()
    for line in fileinput.input():
        res.append([True if c == "@" else False for c in line[:-1]])

    return res


if __name__ == "__main__":
    data = parse()

    P1 = data.cleanup()
    print(f"P1: {P1}")

    P2 = P1
    while (v := data.cleanup()) != 0:
        P2 += v

    print(f"P2: {P2}")
