from collections import Counter
from typing import Hashable

from common.types import Ballot, Result, Scheme
from common.shared_main import shared_main


# borda count depends on the size of the ballot,
# so we will use the length of the longest ballot
# (a completely arbitrary choice)
def borda(ballots: list[Ballot]) -> Result:
    size: int = max(len(ballot.ranking) for ballot in ballots)
    points: list[int] = [c for c in range(size - 1, -1, -1)]
    scores: Counter[Hashable] = Counter()
    for ballot in ballots:
        for i, candidate in enumerate(ballot.ranking):
            scores[candidate] += points[i] * ballot.tally
    max_score: int = max(scores.values())
    winners: list[Hashable] = [
        candidate for candidate, score in scores.items() if score == max_score
    ]
    return winners[0], len(winners) == 1


scheme: Scheme = borda
name: str = "Borda Count"


def main() -> None:
    shared_main("borda", scheme)


if __name__ == "__main__":
    main()
