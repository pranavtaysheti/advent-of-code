import fileinput
from copy import deepcopy
from itertools import compress
from typing import NamedTuple, Self
from collections.abc import Callable


class Instruction(NamedTuple):
    quantity: int
    from_: int
    to: int


class Stacks(list[list[str]]):
    def move_one(self, ins: Instruction):
        for _ in range(ins.quantity):
            self[ins.to-1].append(self[ins.from_-1].pop())

    def move_all_once(self, ins: Instruction):
        self[ins.to-1].extend(self[ins.from_-1][-ins.quantity :])
        self[ins.from_-1] = self[ins.from_-1][: -ins.quantity]

    def solve(self, method: Callable[[Self, Instruction], None]) -> Self:
        new_stacks = deepcopy(self)
        for ins in instructions:
            method(new_stacks, ins)

        return new_stacks

    def top(self) -> str:
        return "".join(stack[-1] for stack in self)


initial_state: Stacks | None = None
instructions: list[Instruction] = []

with fileinput.input() as file:
    for line in file:
        if line[1] == "1":
            break

        if initial_state is None:
            initial_state = Stacks([[] for _ in range(1, len(line), 4)])

        for i, c in enumerate(line[pos] for pos in range(1, len(line), 4)):
            if c == " ":
                continue

            initial_state[i].append(c)

    file.readline()

    for line in file:
        fields = [int(n) for n in compress(line.split(), [0, 1, 0, 1, 0, 1])]
        instructions.append(Instruction(*fields))

assert type(initial_state) == Stacks

for stack in initial_state:
    stack.reverse()

print(f"P1: {initial_state.solve(Stacks.move_one).top()}")
print(f"P2: {initial_state.solve(Stacks.move_all_once).top()}")
