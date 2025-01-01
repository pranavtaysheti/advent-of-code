import fileinput
from copy import deepcopy

type Position = tuple[int, int]
type Layout = list[list[str]]

VECTORS: dict[str, tuple[int, int]] = {
    "^": (-1, 0),
    ">": (0, +1),
    "v": (+1, 0),
    "<": (0, -1),
}

layout: Layout = []
cursor: Position = (-1, -1)
instructions: str = ""


class State:
    def __init__(self):
        self.layout: Layout = deepcopy(layout)
        self.cursor: Position = cursor

    def solve(self):
        for i in instructions:
            c_row, c_col = VECTORS[i]

            row, col = self.cursor
            while (v := self.layout[n_row := row + c_row][n_col := col + c_col]) == "O":
                row, col = n_row, n_col

            if v == "#":
                continue

            self.layout[n_row][n_col] = "O"

            f_row, f_col = self.cursor[0] + c_row, self.cursor[1] + c_col
            self.layout[f_row][f_col] = "."

            self.cursor = f_row, f_col

    def gps_score(self) -> int:
        res = 0
        for i, line in enumerate(self.layout):
            res += sum(100 * i + j for j, c in enumerate(line) if c == "O")

        return res

    def __str__(self) -> str:
        return "\n".join("".join(line) for line in self.layout)


with fileinput.input() as input_file:
    for i, line in enumerate(input_file):
        if len(line) == 1:
            break

        layout.append([c for c in line[:-1]])
        if (j := line.find("@")) >= 0:
            layout[i][j] = "."
            cursor = i, j

    instructions = "".join(line[:-1] for line in input_file)

S1 = State()
S1.solve()

print(f"P1: {S1.gps_score()}")
print(f"P2: {0}")
