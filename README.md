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

### Day 11
Sometimes the only way to work out what trap has been set… is to walk into it.
Brute force part 1 approach predictably got punished, 
but by a simple tripling of the number of iterations it needed to run for rather than any changing of the rules.

By the final iteration of part 2, keeping track of duplicated values together (i.e. with a value and count rather than just a list of values) 
reduced the amount of calculations by a factor of 40 billion, which is a reduction of 180 trillion calculations per cycle!

### Day 13
Vectors! Unless the vectors are parallel, there's only one solution. 
A nice dataclass with some of the dunder methods like `__add__` defined helped.
Could have utilised vector package on pypi alternatively.

The twist for part b wasn't expected, and led to a big re-write and deeper dive into vector calculations.

### Day 14
Spent too long on part 2 - thought the tree would be symmetric, so spent a while checking for symmetry.
Solved quickly the next morning by assuming that the robots would all be grouped together when the tree is formed,
so the product of the number of robots in each sub-area of the grid would be smaller.
A plot showed a potential candidate, which turned out to be correct:
![day_14.png](day_14.png)

### Day 15
Nothing clever here, but a gif of some of part 2:
![day_15_part_2.gif](day_15.gif)

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
