from __future__ import annotations

import fileinput
from collections.abc import Callable
from enum import Enum, auto
from operator import rshift, xor
from typing import NamedTuple


def mod8(o1: int) -> int:
    return o1 % 8


class VirtualMachine:
    class OperandType(Enum):
        Literal = auto()
        Combo = auto()
        RegC = 2

    class Instruction(NamedTuple):
        name: str
        operand_type: VirtualMachine.OperandType
        operator: Callable[[int, int], int] | None | Callable[[int], int]
        first_operand: str | None

    instructions: list[Instruction] = [
        Instruction("adv", OperandType.Combo, rshift, "a"),
        Instruction("bxl", OperandType.Literal, xor, "b"),
        Instruction("bst", OperandType.Combo, mod8, None),
        Instruction("jnz", OperandType.Literal, None, None),
        Instruction("bxc", OperandType.RegC, xor, "b"),  # second operand is c
        Instruction("out", OperandType.Combo, mod8, None),
        Instruction("bdv", OperandType.Combo, rshift, "a"),
        Instruction("cdv", OperandType.Combo, rshift, "a"),
    ]

    def __init__(self) -> None:
        self.cursor = 0
        self.registers = registers

    def execute(self) -> int | None:
        ins = self.instructions[program[self.cursor]]
        res = None

        operand_2 = int(program[self.cursor + 1])
        match ins.operand_type:
            case self.OperandType.Combo:
                if operand_2 > 3:
                    operand_2 = registers[operand_2 - 4]

            case self.OperandType.RegC:
                operand_2 = registers[2]

        def res_register(sol: int):
            if ins.name[0] == "o":
                nonlocal res
                res = sol

            else:
                self.registers[ord(ins.name[0]) - 97] = sol

        if ins.name == "jnz":
            if self.registers[0] != 0:
                self.cursor = operand_2
                return

        else:
            assert ins.operator is not None

            if ins.first_operand is not None:
                operand_1 = self.registers[ord(ins.first_operand) - 97]
                res_register(ins.operator(operand_1, operand_2))
            else:
                res_register(ins.operator(operand_2))

        self.cursor += 2
        return res

    def run_program(self) -> str:
        output = []

        while self.cursor < len(program):
            if (out := self.execute()) is not None:
                output.append(out)

        return ",".join(str(i) for i in output)


with fileinput.input() as input_file:
    registers: list[int] = [
        int(input_file.readline().split()[2]),
        int(input_file.readline().split()[2]),
        int(input_file.readline().split()[2]),
    ]

    input_file.readline()

    program = [int(s) for s in input_file.readline().split()[1].split(",")]

    print(f"P1: {VirtualMachine().run_program()}")
    print(f"P2: {0}")
