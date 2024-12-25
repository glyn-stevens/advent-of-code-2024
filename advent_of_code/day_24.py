import copy
import itertools
import logging
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import TypeAlias
from graphviz import Digraph

from advent_of_code.utils import read_input_stripped, solve, test, parse_args, configure_logging


class GateType(Enum):
    OR = "OR"
    AND = "AND"
    XOR = "XOR"


Id: TypeAlias = str
State: TypeAlias = int | None


@dataclass
class Gate:
    input_1_id: Id
    input_2_id: Id
    output_id: Id
    type_: GateType


@dataclass
class System:
    wires: dict[Id, State]
    gates: list[Gate]

    @property
    def output_decimal(self) -> int:
        return int(self.output_binary, base=2)

    @property
    def output_binary(self) -> str:
        outputs = sorted(
            {id_: state for id_, state in self.wires.items() if id_.startswith("z")}.items(),
            reverse=True,
        )
        binary = "".join(str(wire[1]) for wire in outputs)
        return binary


def main():
    args = parse_args()
    configure_logging(args)
    logging.info(f"Running script {Path(__file__).name}...")
    inputs = parse_inputs(read_input_stripped("day_24.txt"))
    sample_inputs = parse_inputs(read_input_stripped("day_24_sample.txt"))
    test(sample_inputs, part_1, "Part 1 test", expected=2024)
    solve(inputs, part_1, "Part 1")
    inputs = parse_inputs(read_input_stripped("day_24.txt"))
    solve(inputs, part_2, "Part 2")


def parse_inputs(inputs: list[str]) -> System:
    gates = []
    wires: dict[str, int | None] = dict()
    parsing_initial_state = True
    for line in inputs:
        if parsing_initial_state:
            if not line:
                parsing_initial_state = False
                continue
            parts = line.split(":")
            id_ = parts[0]
            wires[id_] = int(parts[1].strip())
        else:
            parts = line.split()
            output_id = parts[4]
            gates.append(Gate(parts[0], parts[2], output_id, GateType(parts[1])))
            wires[output_id] = None
    wire_ids = set(wires.keys())
    assert all(
        (g.input_1_id in wire_ids and g.input_2_id in wire_ids and g.output_id in wire_ids)
        for g in gates
    ), "Some gates with ids missing from wires"
    return System(wires, gates)


def calculate_gate_output(gate: Gate, all_wires: dict[Id, State]) -> int:
    input_1, input_2 = all_wires[gate.input_1_id], all_wires[gate.input_2_id]
    if input_1 is None or input_2 is None:
        raise ValueError
    match gate.type_:
        case GateType.AND:
            result = input_1 and input_2
        case GateType.OR:
            result = input_1 or input_2
        case GateType.XOR:
            result = input_1 != input_2
        case _:
            raise NotImplementedError
    return int(result)


def part_1(system: System) -> int:
    run_system(system)
    logging.info("Finished calculating system")
    return system.output_decimal


def run_system(system: System) -> None:
    while any(w is None for w in system.wires.values()):
        gates_solved_this_loop = False
        for gate in system.gates:
            if system.wires[gate.output_id] is None:
                try:
                    system.wires[gate.output_id] = calculate_gate_output(gate, system.wires)
                except ValueError:
                    continue
                gates_solved_this_loop = True
        if not gates_solved_this_loop:
            raise ValueError("All outputs from system cannot be computed - loops present.")


def number_trailing_digits_correct(actual: str, expected: str) -> int:
    for i, (a, e) in enumerate(zip(reversed(actual), reversed(expected))):
        if a != e:
            return i
    return len(actual)


def score_system(original_system: System, test_numbers: list[tuple[str, str]]) -> int:
    scores = []
    for xy in test_numbers:
        expected = bin(int(xy[0], base=2) + int(xy[1], base=2))[2:]
        system = copy.deepcopy(original_system)
        initialise_wires(system, xy)
        try:
            run_system(system)
        except ValueError:
            return -1
        score = number_trailing_digits_correct(system.output_binary, expected)
        logging.debug(f"Score: {score}. {system.output_binary=}, {expected=} for test: {xy}")
        scores.append(score)
    return min(scores)


def initialise_wires(system: System, x_and_y_binary: tuple[str, str]) -> None:
    x, y = x_and_y_binary
    x_reversed, y_reversed = (
        x[::-1],
        y[::-1],
    )  # Reverse for convenience - the last digits go in inputs x00 and y00
    for id_ in system.wires.keys():
        if id_[0] == "x":
            digit = int(id_[1:])
            system.wires[id_] = int(x_reversed[digit])
        elif id_[0] == "y":
            digit = int(id_[1:])
            system.wires[id_] = int(y_reversed[digit])
        else:
            system.wires[id_] = None


def swap_outputs(system: System, pairs_to_swap: frozenset[tuple[Id, Id]]) -> None:
    for a_id, b_id in pairs_to_swap:
        a_idx = next(idx for (idx, gate) in enumerate(system.gates) if gate.output_id == a_id)
        b_idx = next(idx for (idx, gate) in enumerate(system.gates) if gate.output_id == b_id)
        system.gates[a_idx].output_id = b_id
        system.gates[b_idx].output_id = a_id


def swap_name(swaps: frozenset[tuple[Id, Id]]) -> str:
    return ",".join(f"{x},{y}" for x, y in swaps)


def part_2(original_system: System) -> str:
    visualise_system(original_system)
    test_nums_binary = [
        ("10101" * 9, "10101" * 9),
        ("01010" * 9, "01010" * 9),
        ("1" * 45, "1" * 45),
        ("0" * 45, "0" * 45),
        ("0" * 45, "1" * 45),
        ("1" * 45, "0" * 45),
        ("11000" * 9, "11100" * 9),
        ("00011" * 9, "00111" * 9),
        ("11010" * 9, "01011" * 9),
    ]
    gate_ids = [g.output_id for g in original_system.gates]
    all_output_pairs = list(itertools.combinations(gate_ids, 2))
    swaps_to_test: list[frozenset[tuple[Id, Id]]] = [frozenset({p}) for p in all_output_pairs]
    scores = dict()
    for cycle in range(
        4
    ):  # We know from the puzzle there are 4 pairs of outputs which need swapping
        for i, swaps in enumerate(swaps_to_test):
            if i % 1000 == 0:
                logging.info(f"Cycle: {cycle+1}/4. Loop in cycle: {i}/{len(swaps_to_test)}")
            system = copy.deepcopy(original_system)
            swap_outputs(system, swaps)
            scores[swaps] = score_system(system, test_nums_binary)
        best_swaps = [swaps for swaps, score in scores.items() if score == max(scores.values())]
        logging.info(f"Best score: {max(scores.values())}. Swaps with this score: {best_swaps}")
        swaps_to_test = [
            frozenset([*swaps_done, new_swaps])
            for new_swaps in all_output_pairs
            for swaps_done in best_swaps
        ]
    assert len(best_swaps) == 1, "Got multiple best swaps."
    return swap_name(best_swaps[0])


def visualise_system(system: System) -> None:
    def gate_name(gate: Gate) -> str:
        return f"{gate.type_.value} ({gate.output_id})"

    circuit = Digraph()
    for gate in system.gates:
        circuit.node(gate_name(gate))
    for id_ in system.wires.keys():
        if id_[0] in ["x", "y"]:
            circuit.node(id_)
            for gate in system.gates:
                if gate.input_1_id == id_ or gate.input_2_id == id_:
                    circuit.edge(tail_name=id_, head_name=gate_name(gate))
    for gate in system.gates:
        if gate.output_id[0] == "z":
            circuit.node(gate.output_id)
            circuit.edge(tail_name=gate_name(gate), head_name=gate.output_id)
        else:
            for other in system.gates:
                if other.input_1_id == gate.output_id or other.input_2_id == gate.output_id:
                    circuit.edge(tail_name=gate_name(gate), head_name=gate_name(other))
    circuit.render(filename="day_24_original_circuit", format="png")


if __name__ == "__main__":
    main()
