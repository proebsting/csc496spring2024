from typing import Hashable, NamedTuple, Callable


class Ballot(NamedTuple):
    ranking: tuple[Hashable, ...]
    tally: int


# first element is the winner,
# second element is True if there were no ties during the selection process
Result = tuple[Hashable | None, bool]


class Election(NamedTuple):
    ballots: list[Ballot]
    winners: dict[str, Hashable]


class Corpus(NamedTuple):
    num_candidates: int | None
    num_voters: int | None
    max_ranking_length: int | None
    min_ranking_length: int | None
    max_unique_rankings: int | None
    elections: list[Election]


Scheme = Callable[[list[Ballot]], Result]
