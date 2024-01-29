from collections import Counter
from os import name
from typing import Hashable

from common.types import Ballot, Result, Scheme


# borda count depends on the size of the ballot,
# so we will use the length of the longest ballot
# (a completely arbitrary choice)
def borda(ballots: list[Ballot]) -> Result:
    size: int = max(len(ballot.ranking) for ballot in ballots)
    points: list[int] = [c for c in range(size, 0, -1)]
    scores: Counter[Hashable] = Counter()
    for ballot in ballots:
        for i, candidate in enumerate(ballot.ranking):
            scores[candidate] += points[i]
    max_score: int = max(scores.values())
    winners: list[Hashable] = [
        candidate for candidate, score in scores.items() if score == max_score
    ]
    return winners[0], len(winners) == 1


scheme: Scheme = borda
name: str = "Borda Count"
