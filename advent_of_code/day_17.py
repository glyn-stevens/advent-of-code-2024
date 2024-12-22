import logging
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from advent_of_code.utils import solve, test, parse_args, configure_logging


class Opcode(Enum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7


@dataclass(frozen=True)
class Instruction:
    opcode: Opcode
    operand: int


@dataclass
class Registers:
    a: int
    b: int
    c: int

    def __repr__(self):
        return f"A:{self.a}, B:{self.b}, C:{self.c} ({[bin(r) for r in [self.a, self.b, self.c]]})"


class Machine:
    registers: Registers
    program: list[int]
    pointer: int
    output: list[int]

    def __init__(
        self, register_values: tuple[int, int, int], program: list[int], pointer: int = 0
    ):
        self.registers = Registers(register_values[0], register_values[1], register_values[2])
        self.program = program
        self.pointer = pointer
        self.output = []

    def __repr__(self):
        return f"Registers: {self.registers}, Program: {self.program}, Pointer: {self.pointer}, Output: {self.output}"

    def reset(self, register_values: tuple[int, int, int], pointer: int = 0):
        self.registers = Registers(register_values[0], register_values[1], register_values[2])
        self.pointer = pointer
        self.output = []

    def step(self) -> bool:
        opcode = Opcode(self.program[self.pointer])
        operand = self.program[self.pointer + 1]
        function_map = {
            Opcode.ADV: self.adv,
            Opcode.BDV: self.bdv,
            Opcode.CDV: self.cdv,
            Opcode.OUT: self.out,
            Opcode.JNZ: self.jnz,
            Opcode.BST: self.bst,
            Opcode.BXL: self.bxl,
            Opcode.BXC: self.bxc,
        }
        function = function_map[opcode]
        function(operand)
        self.pointer += 2
        if self.pointer >= len(self.program):
            return True
        return False

    def combo_operand(self, operand: int) -> int:
        if 0 <= operand <= 7:
            return (*range(4), self.registers.a, self.registers.b, self.registers.c)[operand]
        raise ValueError(f"Operand {operand} not expected")

    def adv(self, operand: int) -> None:
        self.registers.a = self._dv(operand)

    def bdv(self, operand: int) -> None:
        self.registers.b = self._dv(operand)

    def cdv(self, operand: int) -> None:
        self.registers.c = self._dv(operand)

    def _dv(self, operand: int) -> int:
        return int(self.registers.a / (2 ** self.combo_operand(operand)))

    def bxl(self, operand: int) -> None:
        self.registers.b = self.registers.b ^ operand

    def bst(self, operand: int) -> None:
        self.registers.b = self.combo_operand(operand) % 8

    def jnz(self, operand: int) -> None:
        if self.registers.a != 0:
            self.pointer = operand - 2

    def bxc(self, _: int) -> None:
        self.registers.b = self.registers.b ^ self.registers.c

    def out(self, operand: int) -> None:
        self.output.append(self.combo_operand(operand) % 8)

    def run_until_completion(self) -> None:
        while True:
            if self.step():
                break

    def run_until_single_output(self) -> None:
        while True:
            self.step()
            if self.output:
                break


def main():
    args = parse_args()
    configure_logging(args)
    logging.info(f"Running script {Path(__file__).name}...")
    input_machine = Machine(
        register_values=(46337277, 0, 0), program=[2, 4, 1, 1, 7, 5, 4, 4, 1, 4, 0, 3, 5, 5, 3, 0]
    )
    sample_inputs = Machine(register_values=(729, 0, 0), program=[0, 1, 5, 4, 3, 0])
    test(sample_inputs, part_1, "Part 1 test", expected="4,6,3,5,6,3,5,2,1,0")
    solve(input_machine, part_1, "Part 1")

    input_machine = Machine(
        register_values=(0, 0, 0), program=[2, 4, 1, 1, 7, 5, 4, 4, 1, 4, 0, 3, 5, 5, 3, 0]
    )
    solve(input_machine, part_2, "Part 2")


def part_1(machine: Machine) -> str:
    logging.info(f"Got machine in initial state {machine}")
    machine.run_until_completion()
    return ",".join([str(x) for x in machine.output])


def part_2(machine: Machine) -> int:
    logging.info(f"Got machine in initial state {machine}")
    matching = find_inputs_so_output_matches_program(machine)
    logging.info(f"Inputs where registry A is equal to: {matching} output exactly the program")
    return min(matching)


def find_inputs_so_output_matches_program(machine: Machine) -> set[int]:
    a_samples = list(range(0, 8))
    for i, next_reqd_output in enumerate(reversed(machine.program)):
        logging.debug(f"Loop {i}: 'A' samples={[bin(p) for p in a_samples]}, {next_reqd_output=}")
        matching_samples = set()
        for register_a in a_samples:
            machine.reset((register_a, 0, 0))
            machine.run_until_single_output()
            if machine.output[0] == next_reqd_output:
                logging.debug(f"Found ({machine.output}). ({bin(register_a)=}")
                matching_samples.add(register_a)
        if not matching_samples:
            raise ValueError(f"No match for digit {i} from the end. Reqd {next_reqd_output}")
        a_samples = [
            binary_append_3_bits(reg_a, suffix)
            for reg_a in matching_samples
            for suffix in range(0, 8)
        ]
    return matching_samples


def binary_append_3_bits(value: int, suffix: int) -> int:
    return int(bin(value)[2:] + bin(suffix)[2:].zfill(3), base=2)


if __name__ == "__main__":
    main()
