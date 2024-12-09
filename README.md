# advent-of-code-2024

Glyn's solutions to the [advent of code 2024 puzzles](https://adventofcode.com/2024), lets see how this goes!

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
### Random thoughts
- Some lessons in "you ain't gonna need it" when doing part 1.
Spent time optimising in areas that, in the end, weren't useful for part 2.

### Day 5
Used bubble sort - a more efficient method would have been possible but the compute time was still very small.

### Day 6
Extremely slow performance in part 2 due to copying the entire grid each time the guard moved.
Regression test not sensible due to performance.
Improvements to do when have more time:
- Store the Area as an (x, y) size, with obstacles and places visited stored as sets of coordinates.
- Find the closest obstacle in the direction the guard is facing, and move immediately there, rather than single steps
  - Note: stepping through 1 space at a time still required for finding shortlist of all the potential obstacle locations for part 2

### Day 7
2^x possible answers for x parameters in the equation didn't seem crazy for part 1,
especially with the max parameters per equation being 12 giving a measly 4096 checks to make.
So, taking a "you ain't gonna need it" approach, got a brute force approach working which was easy to modify for part 2.

But for part 2, up to 531441 calculations would be needed per equation using the brute force,
and the solution did take ~50s to solve using this method.
With some time left, I managed to use tree logic to discount many of the possibilities much earlier in the checking process.
This reduced time from ~50s to under 0.1s.

### Day 8
Good handling of the grid (i.e. just storing the locations of the important items rather than storing the value for each cell in the grid)
helped the solver run very quickly, and a nice `print_grid()` function taking this storage of the grid as inputs still allowed easy debugging.

## Lint
```shell
bin/list.ps1
```

## Tests
Starting from when it got more complex, tests added to prevent regression.
Prior to this, assertions are added after solution is found to allow safe refactoring.
```shell
poetry run pytest
```
