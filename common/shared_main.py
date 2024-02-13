import argparse
from pprint import pprint
from typing import Hashable

from .types import Scheme, Election
from .utility import (
    read_corpus,
    unmarshal_corpus,
    unmarshal_elections,
    write_elections,
    read_election,
)


def do_corpus_file(
    fname: str, name: str, scheme: Scheme, check: bool, overwrite: bool, verbose: bool
):
    with open(fname, "r") as f:
        data = read_corpus(f)
    corpus = unmarshal_corpus(data)
    elections = corpus.elections
    do_elections(name, scheme, check, overwrite, elections, verbose)


def do_elections_file(
    fname: str, name: str, scheme: Scheme, check: bool, overwrite: bool, verbose: bool
):
    with open(fname, "r") as f:
        data = read_corpus(f)
    elections = unmarshal_elections(data)
    do_elections(name, scheme, check, overwrite, elections, verbose)
    if overwrite:
        with open(fname, "w") as f:
            write_elections(elections, f)


def do_election_file(
    fname: str, name: str, scheme: Scheme, check: bool, overwrite: bool, verbose: bool
):
    with open(fname, "r") as f:
        election = read_election(f)
    do_election(name, scheme, check, overwrite, election, verbose)
    if overwrite:
        with open(fname, "w") as f:
            write_elections([election], f)


def do_elections(
    name: str,
    scheme: Scheme,
    check: bool,
    overwrite: bool,
    elections: list[Election],
    verbose: bool,
):
    for election in elections:
        do_election(name, scheme, check, overwrite, election, verbose)


def do_election(
    name: str,
    scheme: Scheme,
    check: bool,
    overwrite: bool,
    election: Election,
    verbose: bool,
):
    result = scheme(election.ballots)
    winner: Hashable = result[0] if result[1] else "<AMBIGUOUS>"
    if verbose:
        pprint(election.ballots, indent=4)
        print(result)
        if name in election.winners:
            print(f"Expected winner: {election.winners[name]}, actual winner: {winner}")
        else:
            print(f"Missing expected winner for {name}")
    if check and name in election.winners and election.winners[name] != winner:
        print(f"Error: {name} winner mismatch")
        pprint(election.ballots, indent=4)
        print(result)
        print(f"Expected winner: {election.winners[name]}, actual winner: {result}")
    if overwrite:
        election.winners[name] = winner


def shared_main(name: str, scheme: Scheme):
    args = parse_args()
    if args.election:
        do_election_file(
            args.election, name, scheme, args.check, args.overwrite, args.verbose
        )
    elif args.elections:
        do_elections_file(
            args.elections, name, scheme, args.check, args.overwrite, args.verbose
        )
    elif args.corpus:
        do_corpus_file(
            args.corpus, name, scheme, args.check, args.overwrite, args.verbose
        )
    else:
        raise ValueError("No input file specified")


def parse_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--election", type=str, help="election file")
    group.add_argument("--elections", type=str, help="elections file")
    group.add_argument("--corpus", type=str, help="corpus file")
    parser.add_argument("--output", type=str, help="output file")
    parser.add_argument(
        "--overwrite", action="store_true", help="overwrite election values"
    )
    parser.add_argument("--verbose", action="store_true", help="print election values")
    parser.add_argument("--check", action="store_true", help="check election values")

    args = parser.parse_args()
    return args
