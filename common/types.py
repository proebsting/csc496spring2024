from typing import Hashable, NamedTuple, Callable


class Ballot(NamedTuple):
    ranking: tuple[Hashable, ...]
    tally: int


# first element is the winner,
# second element is True if there were no ties during the selection process
Result = tuple[Hashable | None, bool]


Scheme = Callable[[list[Ballot]], Result]
