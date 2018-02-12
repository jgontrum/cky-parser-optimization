import argparse
import json
from sys import stderr
from time import time

from pcfg_parser.parser.parser import Parser
from pcfg_parser.parser.pcfg import PCFG

"""
Mostly a copy of parse.py, but with fixed input and without multithreading.
Profiler creates clearer and better interpretable results this way.
"""

def parse(data):
    t0 = time()
    sentence_id, sentence, parser = data
    tree = parser.parse(sentence)
    print(f"Finished {sentence_id}.", file=stderr)
    return json.dumps(tree), time() - t0


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--grammar", help="Path to grammar file.",
                        type=str, required=True)

    args = parser.parse_args()

    grammar_file = args.grammar

    print("Loading grammar from " + grammar_file + " ...", file=stderr)

    pcfg = PCFG()
    pcfg.load_model(open(grammar_file))
    parser = Parser(pcfg)

    print("Parsing sentences ...", file=stderr)

    sentences = [
        "Champagne and dessert followed .",
        "The governor could n't make it , so the lieutenant governor welcomed the special guests .",
        "He had been a sales and marketing executive with Chrysler for 20 years .",
        "Champagne and dessert followed .",
        "The governor could n't make it , so the lieutenant governor welcomed the special guests .",
        "He had been a sales and marketing executive with Chrysler for 20 years .",
        "Champagne and dessert followed .",
        "The governor could n't make it , so the lieutenant governor welcomed the special guests .",
        "He had been a sales and marketing executive with Chrysler for 20 years ."
    ]

    print(f"Received {len(sentences)} sentences...", file=stderr)

    input = [
        (i, sentence, parser) for i, sentence in enumerate(sentences)
    ]

    output = [parse(s) for s in input]

    runtime = 0
    for sentence, t in output:
        runtime += t
        print(sentence)

    print("Time: (%.2f)s    \n" % runtime, file=stderr)


if __name__ == "__main__":
    main()
