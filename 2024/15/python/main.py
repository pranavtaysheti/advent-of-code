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
        self.box = "O"

    def check_line(self, i: str) -> tuple[Position, bool]:
        c_row, c_col = VECTORS[i]

        row, col = self.cursor
        while (
            v := self.layout[n_row := row + c_row][n_col := col + c_col]
        ) in self.box:
            row, col = n_row, n_col

        match v:
            case "#":
                return (n_row, n_col), False
            case ".":
                return (n_row, n_col), True

        raise AssertionError(f"v should be # or .: {v}")

    def solve(self):
        for i in instructions:
            (n_row, n_col), ok = self.check_line(i)
            if not ok:
                continue

            self.layout[n_row][n_col] = "O"

            c_row, c_col = VECTORS[i]
            f_row, f_col = self.cursor[0] + c_row, self.cursor[1] + c_col

            self.layout[f_row][f_col] = "."
            self.cursor = f_row, f_col

    def gps_score(self) -> int:
        res = 0
        for i, line in enumerate(self.layout):
            res += sum(100 * i + j for j, c in enumerate(line) if c == self.box[0])

        return res

    def __str__(self) -> str:
        layout = deepcopy(self.layout)
        layout[self.cursor[0]][self.cursor[1]] = "@"

        return "\n".join("".join(line) for line in layout)


class ExpandedState(State):
    def __init__(self):
        super().__init__()

        self.layout = [[] for _ in range(len(layout))]
        for i, line in enumerate(layout):
            self.layout[i] = ["." for _ in range(len(layout[0]) * 2)]

            for j, c in enumerate(line):
                if c == "O":
                    self.layout[i][2 * j], self.layout[i][2 * j + 1] = "[", "]"

                else:
                    self.layout[i][2 * j], self.layout[i][2 * j + 1] = c, c

        self.cursor = cursor[0], cursor[1] * 2
        self.box = "[]"

    def check_tree(self, ins: str) -> list[set[int]] | None:
        c_row, _ = VECTORS[ins]

        elems: list[set[int]] = [{self.cursor[1]}]
        z_row = self.cursor[0] + c_row
        while len(elems[-1]) > 0:
            next_elems = set()

            for c in elems[-1]:
                match (self.layout[z_row][c]):
                    case "[":
                        next_elems.add(c + 1)
                        next_elems.add(c)
                    case "]":
                        next_elems.add(c - 1)
                        next_elems.add(c)
                    case "#":
                        return None

            elems.append(next_elems)
            z_row += c_row

        return elems[:-1]

    def solve(self):
        for ins in instructions:
            row, col = self.cursor
            c_row, c_col = VECTORS[ins]
            f_row, f_col = row + c_row, col + c_col
            match ins:
                case "<" | ">":
                    (_, l_col), ok = self.check_line(ins)
                    if not ok:
                        continue

                    for i, c in enumerate(range(f_col + c_col, l_col + c_col, c_col)):
                        match (c_col, i % 2):
                            case [1, 0] | [-1, 1]:
                                self.layout[row][c] = "["
                            case [1, 1] | [-1, 0]:
                                self.layout[row][c] = "]"

                case "^" | "v":
                    elems = self.check_tree(ins)
                    if elems is None:
                        continue

                    z_row = row + c_row * len(elems)
                    for cols in reversed(elems):
                        for c in cols:
                            self.layout[z_row][c] = self.layout[z_row - c_row][c]
                            self.layout[z_row - c_row][c] = "."

                        z_row -= c_row

            self.layout[f_row][f_col] = "."
            self.cursor = f_row, f_col


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

S2 = ExpandedState()
S2.solve()
print(f"P2: {S2.gps_score()}")
