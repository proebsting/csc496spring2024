import sys
import json
from typing import Any, Hashable
from io import TextIOWrapper

from .types import Ballot, Election, Corpus


def pretty_ballot_json(ballot: Ballot) -> str:
    return f'{{ "count":{ballot.tally:3}, "ranking": {list(ballot.ranking)} }}'


def pretty_election_json(election: Election) -> str:
    prologue = '{ "ballots": [\n'
    ballots = ",\n".join(pretty_ballot_json(b) for b in election.ballots)
    epilogue = f'],\n"winners": {json.dumps(election.winners,sort_keys=True)} }}'
    return prologue + ballots + epilogue


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


def unmarshal_corpus(data: Any) -> Corpus:
    return Corpus(
        num_candidates=data["num_candidates"],
        num_voters=data["num_voters"],
        max_ranking_length=data["max_ranking_length"],
        min_ranking_length=data["min_ranking_length"],
        max_unique_rankings=data["max_unique_rankings"],
        elections=elections_from_corpus(data),
    )


def elections_from_corpus(data: Any) -> list[Election]:
    return [unmarshal_election(election) for election in data["elections"]]


def unmarshal_elections(data: Any) -> list[Election]:
    return [unmarshal_election(election) for election in data]


def write_elections(elections: list[Election], f: TextIOWrapper):
    f.write("[\n")
    f.write(",\n".join(pretty_election_json(election) for election in elections))
    f.write("\n]\n")


def write_corpus(corpus: Any, f: TextIOWrapper):
    json.dump(corpus, f, indent=4)


def marshal_ballot(ballot: Ballot) -> dict[str, Any]:
    return {"ranking": list(ballot.ranking), "count": ballot.tally}


def marshal_election(election: Election) -> dict[str, Any]:
    return {
        "ballots": [marshal_ballot(b) for b in election.ballots],
        "winners": election.winners,
    }


def unmarshal_ballot(ballot: dict[str, Any]):
    return Ballot(tuple(ballot["ranking"]), ballot["count"])


def unmarshal_election(data: Any) -> Election:
    return Election(
        [unmarshal_ballot(b) for b in data["ballots"]],
        data["winners"] if "winners" in data else {},
    )


def read_list_of_ballots(f: TextIOWrapper) -> list[Ballot]:
    data = json.load(f)
    return [unmarshal_ballot(b) for b in data]


def json_to_Election(data: Any) -> Election:
    ballots = [unmarshal_ballot(b) for b in data["ballots"]]
    winners: dict[str, Hashable] = data["winners"] if "winners" in data else {}
    return Election(ballots, winners)


def read_election(f: TextIOWrapper) -> Election:
    data = json.load(f)
    election = json_to_Election(data)
    return election


def main():
    tiow = TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
    data = read_corpus(tiow)
    check_corpus_consistency(data)


if __name__ == "__main__":
    main()
