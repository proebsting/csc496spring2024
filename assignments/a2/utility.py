import sys
import json
import argparse
from dataclasses import dataclass
from typing import Any
from io import StringIO

from common import Ballot


def read_corpus(f):
    data = json.load(f)
    for election in data["elections"]:
        ballots = election["ballots"]
        voters = sum(b["count"] for b in ballots)
        unique_rankings = len(set(tuple(b["ranking"]) for b in ballots))
        candidates = len(set(c for b in ballots for c in b["ranking"]))
        max_ranking_length = max(len(b["ranking"]) for b in ballots)
        min_ranking_length = min(len(b["ranking"]) for b in ballots)

        assert voters == data["num_voters"]
        assert unique_rankings <= data["max_unique_rankings"]
        assert max_ranking_length <= data["max_ranking_length"]
        assert min_ranking_length >= data["min_ranking_length"]
        assert candidates == data["num_candidates"]

    return data


def write_corpus(corpus: Any, f):
    json.dump(corpus, f, indent=4)


def marshal_ballot(ballot: Ballot):
    return {"ranking": list[ballot.ranking], "count": ballot.tally}


def unmarshal_ballot(ballot: dict[str, Any]):
    return Ballot(tuple(ballot["ranking"]), ballot["count"])


def main():
    read_corpus(sys.stdin)


if __name__ == "__main__":
    main()
