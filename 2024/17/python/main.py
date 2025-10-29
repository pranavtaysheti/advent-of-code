import fileinput
from collections.abc import Callable
from enum import Enum, auto
from itertools import product
from operator import and_, rshift, xor
from typing import NamedTuple


class OperandType(Enum):
    Literal = auto()
    Combo = auto()
    RegC = auto()


class InstructionW0(NamedTuple):
    name: str


class InstructionW2(NamedTuple):
    name: str
    operand_type: OperandType
    operator: Callable[[int, int], int]
    first_operand: int


class VirtualMachine:
    type Instruction = InstructionW0 | InstructionW2

    instructions: list[Instruction] = [
        InstructionW2("adv", OperandType.Combo, rshift, 4),
        InstructionW2("bxl", OperandType.Literal, xor, 5),
        InstructionW2("bst", OperandType.Combo, and_, 7),
        InstructionW0("jnz"),
        InstructionW2("bxc", OperandType.RegC, xor, 5),  # second operand is c
        InstructionW2("out", OperandType.Combo, and_, 7),
        InstructionW2("bdv", OperandType.Combo, rshift, 4),
        InstructionW2("cdv", OperandType.Combo, rshift, 4),
    ]

    def __init__(self, program: list[int], regs: tuple[int, int, int]) -> None:
        self.program = program
        self.registers = [0, 1, 2, 3, *regs, 7]

    def exec_ins(self, cursor: int) -> tuple[int | None, int]:
        ins = self.instructions[program[cursor]]
        out: int | None = None

        def write(sol: int):
            nonlocal out
            if ins.name[0] == "o":
                out = sol

            else:
                self.registers[ord(ins.name[0]) - 93] = sol

        operand_2 = int(program[cursor + 1])
        if ins.name == "jnz":
            if self.registers[4] != 0:
                return (out, operand_2)
        else:
            assert not isinstance(ins, InstructionW0)
            match ins.operand_type:
                case OperandType.Combo:
                    operand_2 = self.registers[operand_2]

                case OperandType.RegC:
                    operand_2 = self.registers[6]

            if isinstance(ins, InstructionW2):
                operand_1 = self.registers[ins.first_operand]
                write(ins.operator(operand_1, operand_2))
            else:
                write(ins.operator(operand_2))

        return out, cursor + 2

    def run_out(self) -> int:
        cursor = 0
        res = None
        while res is None:
            out, n_ins = self.exec_ins(cursor)
            if out is not None:
                res = out

            cursor = n_ins

        return res

    def run_program(self) -> list[int]:
        cursor = 0
        output: list[int] = []
        while cursor < len(program):
            out, n_ins = self.exec_ins(cursor)
            if out is not None:
                output.append(out)

            cursor = n_ins

        return output


def find_inp(program: list[int], out_req: list[int]) -> list[int]:
    res: list[int] = [0]
    for o in reversed(out_req):
        n_res: list[int] = []
        for app, num in product(range(8), res):
            n_num = (num << 3) + app
            vm = VirtualMachine(program, (n_num, 0, 0))
            if vm.run_out() == o:
                n_res.append(n_num)

        res = n_res

    return res


with fileinput.input() as input_file:
    regs: tuple[int, int, int] = (
        int(input_file.readline().split()[2]),
        int(input_file.readline().split()[2]),
        int(input_file.readline().split()[2]),
    )

    input_file.readline()

    program = [int(s) for s in input_file.readline().split()[1].split(",")]

    vm = VirtualMachine(program, regs)
    print(f"P1: {",".join(str(i) for i in vm.run_program())}")

    print(f"P2: {min(find_inp(program, program))}")
