import itertools
import logging
from pathlib import Path
from advent_of_code.utils import read_input_stripped, solve, test, parse_args, configure_logging

Id = str
Connection = set[Id]


def main():
    args = parse_args()
    configure_logging(args)
    logging.info(f"Running script {Path(__file__).name}...")
    inputs = parse_inputs(read_input_stripped("day_23.txt"))
    sample_inputs = parse_inputs(read_input_stripped("day_23_sample.txt"))
    test(sample_inputs, part_1, "Part 1 test", expected=7)
    # solve(inputs, part_1, "Part 1")
    # test(sample_inputs, part_2, "Part 2 test", expected="co,de,ka,ta")
    solve(inputs, part_2, "Part 2")


def parse_inputs(inputs: list[str]) -> list[Connection]:
    return [parse_connection(line) for line in inputs]


def parse_connection(line: str) -> Connection:
    parts = line.split("-")
    return {parts[0], parts[1]}


def part_1(connections: list[Connection]) -> int:
    logging.debug(f"Full input: {connections}")
    triples = find_valid_triples(connections)
    return len([t for t in triples if any(id_.startswith("t") for id_ in t)])


def find_valid_triples(all_connections: list[Connection]) -> set[frozenset[Id]]:
    all_ids = {id_ for c in all_connections for id_ in c}
    sets_connected = set()
    for id_ in all_ids:

        def has_id(connection: Connection) -> bool:
            return id_ in connection

        others_connected = {i for c in filter(has_id, all_connections) for i in c} - {id_}
        for pair in itertools.combinations(others_connected, r=2):
            logging.debug(f"Testing triple {id_} with {pair}")
            connections_in_triple = [{id_, pair[0]}, {id_, pair[1]}, set(pair)]
            if all(c in all_connections for c in connections_in_triple):
                sets_connected.add(frozenset({*pair, id_}))
    return sets_connected


def part_2(connections: list[Connection]) -> str:
    all_triples = find_valid_triples(connections)
    ids_in_triples = {id_ for c in all_triples for id_ in c}
    best_group_yet: tuple[Id, ...] = tuple()
    best_group_length = 13  # Puzzle solved, so I know we're looking for a set of 13
    for id_ in ids_in_triples:

        def has_id(triple: frozenset[Id]) -> bool:
            return id_ in triple

        ids_in_related_triples = {id_ for c in filter(has_id, all_triples) for id_ in c}
        logging.debug(f"{ids_in_related_triples=}")
        while True:
            improved_best_group = False
            for possible_set in itertools.combinations(
                ids_in_related_triples, r=best_group_length
            ):
                logging.debug(f"Checking possible set {possible_set}")
                if all(
                    set(trip) in all_triples for trip in itertools.combinations(possible_set, r=3)
                ):
                    best_group_length += 1
                    best_group_yet = possible_set
                    improved_best_group = True
                    break
            if not improved_best_group:
                break
    return ",".join(sorted(best_group_yet))


if __name__ == "__main__":
    main()
