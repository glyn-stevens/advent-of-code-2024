from dataclasses import dataclass
from pathlib import Path
from advent_of_code.utils import read_input_stripped, solve, test


@dataclass
class InitialFile:
    size: int
    id: int
    space_proceeding: int

    def __repr__(self):
        return f"id:{self.id}, size:{self.size}, space_after:{self.space_proceeding}\n"


def main():
    print(f"Running script {Path(__file__).name}...")
    inputs = parse_inputs(read_input_stripped("day_9.txt"))
    sample_inputs = parse_inputs(["2333133121414131402"])
    test(sample_inputs, part_1, "Part 1 test", expected=1928)
    solve(inputs, part_1, "Part 1")
    test(sample_inputs, part_2, "Part 2 test", expected=2858)
    solve(inputs, part_2, "Part 2")


def parse_inputs(inputs: list[str]) -> list[InitialFile]:
    files = []
    disk_map = inputs[0]
    for i in range(0, len(disk_map), 2):
        space_proceeding = (
            0 if i >= len(disk_map) - 1 else int(disk_map[i + 1])
        )  # No space after final file
        files.append(
            InitialFile(size=int(disk_map[i]), id=int(i / 2), space_proceeding=space_proceeding)
        )
    return files


def compact_files_with_fragmentation(files_to_compact: list[InitialFile]) -> list[int]:
    """Output in dense format as block id in order"""
    output = []
    file_to_move = files_to_compact.pop(-1)  # We're backfilling with the last file first
    while files_to_compact:
        # Remove first file from list to compact and add it to output
        file_staying_in_orig_pos = files_to_compact.pop(0)
        output.extend([file_staying_in_orig_pos.id] * file_staying_in_orig_pos.size)

        # Fill any free space after the file just added to the output with files from the end of the input list
        space_available = file_staying_in_orig_pos.space_proceeding
        while space_available > 0:
            if space_available >= file_to_move.size:
                space_available -= file_to_move.size
                output.extend([file_to_move.id] * file_to_move.size)
                file_to_move.size = 0
                try:
                    file_to_move = files_to_compact.pop(-1)
                except IndexError:
                    # No more files to compact
                    break
            else:
                # File to move doesn't completely fit in space available - fill the space with part of the file
                output.extend([file_to_move.id] * space_available)
                file_to_move.size -= space_available
                space_available = 0
    output.extend([file_to_move.id] * file_to_move.size)
    return output


def checksum(compacted_files: list[int]) -> int:
    return sum(idx * val for idx, val in enumerate(compacted_files))


def compact_files_without_fragmentation(files_to_compact: list[InitialFile]) -> list[int]:
    for file in reversed(files_to_compact):
        pass
        # TODO: complete
    return [0]


def part_1(inputs: list[InitialFile]) -> int:
    compacted = compact_files_with_fragmentation(inputs)
    return checksum(compacted)


def part_2(inputs: list[InitialFile]) -> int:
    compacted = compact_files_without_fragmentation(inputs)
    return checksum(compacted)


if __name__ == "__main__":
    main()
