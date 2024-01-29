import sys
import json
from typing import Any
from io import TextIOWrapper

from .types import Ballot


def check_corpus(
    data: Any,
    num_candidates: int,
    num_voters: int,
    max_ranking_length: int,
    min_ranking_length: int,
    max_unique_rankings: int,
):
    assert data["num_candidates"] == num_candidates
    assert data["num_voters"] == num_voters
    assert data["max_ranking_length"] == max_ranking_length
    assert data["min_ranking_length"] == min_ranking_length
    assert data["max_unique_rankings"] == max_unique_rankings

    for election in data["elections"]:
        ballots = election["ballots"]
        check_ballots(
            num_candidates,
            num_voters,
            max_ranking_length,
            min_ranking_length,
            max_unique_rankings,
            ballots,
        )


def check_ballots(
    num_candidates: int,
    num_voters: int,
    max_ranking_length: int,
    min_ranking_length: int,
    max_unique_rankings: int,
    ballots: list[dict[str, Any]],
):
    assert all(len(b["ranking"]) <= max_ranking_length for b in ballots)
    assert all(len(b["ranking"]) >= min_ranking_length for b in ballots)
    assert len(set(c for b in ballots for c in b["ranking"])) <= num_candidates
    assert len(set(tuple(b["ranking"]) for b in ballots)) <= max_unique_rankings
    assert sum(b["count"] for b in ballots) == num_voters
    assert all(b["count"] >= 0 for b in ballots)
    assert all(len(b["ranking"]) == len(set(b["ranking"])) for b in ballots)


def check_corpus_consistency(data: Any):
    num_voters = data["num_voters"]
    num_candidates = data["num_candidates"]
    max_ranking_length = data["max_ranking_length"]
    min_ranking_length = data["min_ranking_length"]
    max_unique_rankings = data["max_unique_rankings"]

    check_corpus(
        data,
        num_candidates,
        num_voters,
        max_ranking_length,
        min_ranking_length,
        max_unique_rankings,
    )


def read_corpus(f: TextIOWrapper):
    data = json.load(f)
    return data


def write_corpus(corpus: Any, f):
    json.dump(corpus, f, indent=4)


def marshal_ballot(ballot: Ballot):
    return {"ranking": list[ballot.ranking], "count": ballot.tally}


def unmarshal_ballot(ballot: dict[str, Any]):
    return Ballot(tuple(ballot["ranking"]), ballot["count"])


def main():
    tiow = TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
    data = read_corpus(tiow)
    check_corpus_consistency(data)


if __name__ == "__main__":
    main()
