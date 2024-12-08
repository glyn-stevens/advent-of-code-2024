# advent-of-code-2024

Glyn's advent of code 2024, lets see how this goes!

Assertions to be equal to the answers are added after solution is found to allow safe refactoring.

## Setup
Using poetry for package management. To setup venv folder with environment:
```shell
poetry install
```

## Use
One file per day to be run as script.

Run with, for example:
```shell
poetry run python advent_of_code/day_1.py
```

## Notes
### Day 5
Used bubble sort - a more efficient method would have been possible but the compute time was still very small.

### Day 6
Extremely slow performance in part 2 due to copying the entire grid each time the guard moved.
Regression test not sensible due to performance.
Improvements to do when have more time:
- Store the Area as an (x, y) size, with obstacles and places visited stored as sets of coordinates.
- Find the closest obstacle in the direction the guard is facing, and move immediately there, rather than single steps
  - Note: stepping through 1 space at a time still required for finding shortlist of all the potential obstacle locations for part 2

## Lint
```shell
bin/list.ps1
```
