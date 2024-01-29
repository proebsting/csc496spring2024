from io import StringIO, TextIOWrapper
import os
import argparse
from math import factorial
from tokenize import String
from typing import Text

from common.utility import read_corpus, check_corpus


def generate_corpus(
    py: str,
    num_candidates: int,
    num_voters: int,
    max_ranking_length: int,
    min_ranking_length: int,
    max_unique_rankings: int,
    fname: str,
):
    command = (
        f"python3 {py}"
        + f" --num-candidates {num_candidates}"
        + f" --num-voters {num_voters}"
        + f" --max-ranking-length {max_ranking_length}"
        + f" --min-ranking-length {min_ranking_length}"
        + f" --max-unique-rankings {max_unique_rankings}"
        + f" --output-file {fname}"
    )
    # print(command, file=sys.stderr)
    os.system(command)


def main():
    args = parse_args()
    num_candidates: int
    num_voters: int
    max_ranking_length: int
    min_ranking_length: int
    max_unique_rankings: int

    dir = args.tmpdir
    py = args.python_src

    attempts = 0
    passed = 0

    for num_candidates in range(3, 8):
        for num_voters in [5, 50, 500]:
            for min_ranking_length in range(1, min(5, num_candidates)):
                for additional in range(min(3, num_candidates - min_ranking_length)):
                    max_ranking_length = min_ranking_length + additional
                    xcombos: int = factorial(num_candidates) // (
                        factorial(max_ranking_length)
                        * factorial(num_candidates - max_ranking_length)
                    )
                    ycombos: int = factorial(num_candidates) // (
                        factorial(min_ranking_length)
                        * factorial(num_candidates - min_ranking_length)
                    )
                    for max_unique_rankings in range(3, max(xcombos, ycombos)):
                        for num_elections in [1, 5, 10]:
                            for i in range(1):
                                attempts += 1
                                status = do_test(
                                    py,
                                    num_candidates,
                                    num_voters,
                                    max_ranking_length,
                                    min_ranking_length,
                                    max_unique_rankings,
                                    num_elections,
                                    i,
                                    dir,
                                )
                                passed += status
                                print(f"Passed {passed}/{attempts}")


def do_test(
    py: str,
    num_candidates: int,
    num_voters: int,
    max_ranking_length: int,
    min_ranking_length: int,
    max_unique_rankings: int,
    num_elections: int,
    i: int,
    dir: str,
):
    fname = (
        f"corpus_candidates={num_candidates}"
        + f"_voters={num_voters}"
        + f"_max-length={max_ranking_length}"
        + f"_min-length={min_ranking_length}"
        + f"_max-rankings={max_unique_rankings}"
        + f"_elections={num_elections}"
        + f"_{i}.json"
    )
    fname = os.path.join(dir, fname)
    # print(fname)
    generate_corpus(
        py,
        num_candidates,
        num_voters,
        max_ranking_length,
        min_ranking_length,
        max_unique_rankings,
        fname,
    )
    try:
        stream: TextIOWrapper
        with open(fname, "r") as stream:
            data = read_corpus(stream)
            check_corpus(
                data,
                num_candidates,
                num_voters,
                max_ranking_length,
                min_ranking_length,
                max_unique_rankings,
            )
        status = 1
    except:
        print(f"Failed {fname}")
        status = 0
    return status


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--tmpdir", type=str, default="/tmp/", help="Directory to store generated files"
    )
    parser.add_argument(
        "--python_src", type=str, default="./generator.py", help="Python file to run"
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
