from collections import UserString
from copy import copy
from dataclasses import dataclass
from itertools import product
from pprint import pprint
from typing import Self


@dataclass(slots=True, frozen=True)
class Vector:
    row: int
    col: int

    def __sub__(self, e: Self) -> Self:
        return type(self)(self.row - e.row, self.col - e.col)

    def __add__(self, d: Self) -> Self:
        return type(self)(self.row + d.row, self.col + d.col)


class Keypad:
    def __init__(self, layout: list[list[str]], start: Vector):
        self.layout = layout
        self.start = start

    def find_button(self, b: str) -> Vector:
        for i, row in enumerate(self.layout):
            for j, c in enumerate(row):
                if c == b:
                    return Vector(i, j)

        raise AssertionError(f"{b} not found")

    def simulate(self, start: Vector, comm: str) -> bool:
        dir_vec = {
            "<": Vector(0, -1),
            ">": Vector(0, +1),
            "^": Vector(-1, 0),
            "v": Vector(+1, 0),
            "A": Vector(0, 0),
        }

        c_pos = start
        for c in comm:
            e_pos = c_pos + dir_vec[c]
            if self.layout[e_pos.row][e_pos.col] == " ":
                return False

            c_pos = e_pos

        return True


robot_keypad = Keypad(
    layout=[
        [" ", "^", "A"],
        ["<", "v", ">"],
    ],
    start=Vector(0, 2),
)


class Command(UserString):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keypad = robot_keypad

    def expand(self: Self) -> list["ParsedCommand"]:
        comm = self + "A"
        prev_res: list[ParsedCommand] = [ParsedCommand()]
        res: list[ParsedCommand] = []
        c_pos = self.keypad.start
        for c in comm:
            e_pos = self.keypad.find_button(str(c))
            d_vec = e_pos - c_pos
            d_comms = set(gen_commands((d_vec.row, d_vec.col)))
            for p_comm in prev_res:
                for d_comm in d_comms:
                    if not self.keypad.simulate(c_pos, d_comm):
                        continue

                    n_comm = copy(p_comm)
                    n_comm[d_comm] = n_comm.setdefault(d_comm, 0) + 1
                    res.append(n_comm)

            c_pos = e_pos
            prev_res = res
            res = []

        return prev_res


class ParsedCommand(dict[str, int]):
    def cost(self) -> int:
        res: int = 0
        for exp, qty in self.items():
            res += len(exp) * qty + qty

        return res

    def expanded_cost(self, em: dict[str, int]) -> int:
        res: int = 0
        for sub, qty in self.items():
            res += qty * em[sub]

        return res


possiblities: list[tuple[int, int]] = [
    i for i in product(range(-1, +2, 1), range(-2, +3, 1))
]


def gen_commands(p: tuple[int, int]) -> tuple[str, str]:
    ver, hor = p

    hor_exp = ""
    ver_exp = ""
    if hor < 0:
        hor_exp = "".join("<" for _ in range(abs(hor)))
    if hor > 0:
        hor_exp = "".join(">" for _ in range(abs(hor)))
    if ver < 0:
        ver_exp = "".join("^" for _ in range(abs(ver)))
    if ver > 0:
        ver_exp = "".join("v" for _ in range(abs(ver)))

    return hor_exp + ver_exp, ver_exp + hor_exp


def find_smallest(comms: list[ParsedCommand]) -> tuple[list[ParsedCommand], int]:
    min_cost = float("inf")
    min_items: list[ParsedCommand] = []
    for comm in comms:
        if (l := comm.cost()) <= min_cost:
            if l < min_cost:
                min_items = []

            min_items.append(comm)
            min_cost = l

    assert isinstance(min_cost, int)
    return min_items, min_cost


res: dict[str, tuple[list[ParsedCommand], int]] = {}
for p in possiblities:
    hv, vh = gen_commands(p)
    res[vh] = find_smallest(Command(vh).expand())
    res[hv] = find_smallest(Command(hv).expand())

em = {k: v[1] for k, v in res.items()}
res2 = {}
for _ in range(2):
    res2.clear()
    for c, (comms, cost) in res.items():
        min_cost = float("inf")
        min_items: list[ParsedCommand] = []
        for comm in comms:
            if (l := comm.expanded_cost(em)) <= min_cost:
                if l < min_cost:
                    min_items = []

                min_items.append(comm)
                min_cost = l

        assert isinstance(min_cost, int)
        res2[c] = min_items, min_cost

    em = {k: v[1] for k, v in res2.items()}

pprint({k: v[0][0] for k, v in res2.items()})
