import fileinput
from collections.abc import Callable
from enum import Enum, auto
from operator import and_, rshift, xor
from typing import NamedTuple


class OperandType(Enum):
    Literal = auto()
    Combo = auto()
    RegC = auto()


class Instruction_W0(NamedTuple):
    name: str


class Instruction_W2(NamedTuple):
    name: str
    operand_type: OperandType
    operator: Callable[[int, int], int]
    first_operand: int


class VirtualMachine:
    type Instruction = Instruction_W0 | Instruction_W2

    instructions: list[Instruction] = [
        Instruction_W2("adv", OperandType.Combo, rshift, 4),
        Instruction_W2("bxl", OperandType.Literal, xor, 5),
        Instruction_W2("bst", OperandType.Combo, and_, 7),
        Instruction_W0("jnz"),
        Instruction_W2("bxc", OperandType.RegC, xor, 5),  # second operand is c
        Instruction_W2("out", OperandType.Combo, and_, 7),
        Instruction_W2("bdv", OperandType.Combo, rshift, 4),
        Instruction_W2("cdv", OperandType.Combo, rshift, 4),
    ]

    def __init__(self) -> None:
        self.cursor = 0
        self.registers = [0, 1, 2, 3, *registers, 7]

    def execute(self) -> int | None:
        ins = self.instructions[program[self.cursor]]
        res = None

        def write(sol: int):
            if ins.name[0] == "o":
                nonlocal res
                res = sol

            else:
                self.registers[ord(ins.name[0]) - 93] = sol

        operand_2 = int(program[self.cursor + 1])
        if ins.name == "jnz":
            if self.registers[4] != 0:
                self.cursor = operand_2
                return
        else:
            assert not isinstance(ins, Instruction_W0)
            match ins.operand_type:
                case OperandType.Combo:
                    operand_2 = self.registers[operand_2]

                case OperandType.RegC:
                    operand_2 = self.registers[6]

            if isinstance(ins, Instruction_W2):
                operand_1 = self.registers[ins.first_operand]
                write(ins.operator(operand_1, operand_2))
            else:
                write(ins.operator(operand_2))

        self.cursor += 2
        return res

    def run_program(self) -> bytearray:
        output = bytearray()
        while self.cursor < len(program):
            if (out := self.execute()) is not None:
                output.append(out)

        return output


with fileinput.input() as input_file:
    registers: list[int] = [
        int(input_file.readline().split()[2]),
        int(input_file.readline().split()[2]),
        int(input_file.readline().split()[2]),
    ]

    input_file.readline()

    program = [int(s) for s in input_file.readline().split()[1].split(",")]

    print(f"P1: {",".join(str(i) for i in VirtualMachine().run_program())}")
    print(f"P2: {0}")
