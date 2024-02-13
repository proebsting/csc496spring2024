# Assignments #2-N: Implementing RCV Schemes

## Due: 3:00pm on Fridays

1. 2/23: IRV, River, Black, Copeland
2. 3/1: Bucklin, Smith/IRV, Nansens
3. 3/15: Dodgsons, Schulze, Sri-Lanken Contingency
4. 3/22: Kemeny Young, Coombs, Baldwin
5. 3/29: Tideman, BTR-IRV, Minimax

## Assignment Overview

In this assignment, you will write a Python functions that implement various ranked-choice voting schemes.

Each function must match the `Scheme` type from `common/types.py`:

```python
class Ballot(NamedTuple):
    ranking: tuple[Hashable, ...]
    tally: int

# first element is the winner,
# second element is True if there were no ties during the selection process
Result = tuple[Hashable | None, bool]

class Election(NamedTuple):
    ballots: list[Ballot]
    winners: dict[str, Hashable]

Scheme = Callable[[list[Ballot]], Result]
```

The `Scheme` type is a function that takes a list of `Ballot` objects and returns a `Result` object. The `Result` object is a tuple with the first element being the winner of the election and the second element being a boolean indicating whether there were any ties during the selection process.  (The winner is ignored if there were ties.)

Therefore, implementations should have the following import statement:

```python
from common.types import Scheme
```

## Naming the function

The function should be named after the scheme it implements in all lower-case.  For example, the function implementing the Instant Runoff Voting scheme should be named `irv`.  If the scheme has multiple words, the function should be named using underscores.  For example, `smith_irv` for the Smith/IRV scheme.

## `main()`

You do not need to have a `main()` function in your file, and your file  should not execute any code when imported.

That said, it's a good idea to have a `main()` function in your file that you can use to test your implementation.  You may find `common.shared_main.shared_main` helpful for this purpose.

## Python requirements

You must use Python 3.11 or later.

You must format your code with `black`.

Your code must not produce any errors or warnings when run with `mypy --strict`.

## Python assistance

To keep your directory structure under control, you may want to exploit the `PYTHONPATH` environment variable in order to have convenient access to the `common` package.  


## Code sharing

While you may not share code with other students, you may discuss the assignment with other students.

You may also share code that is meant to test your program. For example, you may share code that reads the JSON file and verifies that the election is valid given the parameters.
