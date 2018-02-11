import argparse
import json
from sys import stderr
from time import time

from pcfg_parser.treebank.grammar_extractor import GrammarExtractor

"""
Base code copied from given starter code.
-> http://stp.lingfil.uu.se/~sara/kurser/parsing18/pcfg_parsing.html
"""

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--treebank", help="Path to read treebank file from.",
                        type=str, required=True)
    parser.add_argument("--grammar", help="Path to write grammar file to.",
                        type=str, required=False,
                        default="grammar.txt")

    args = parser.parse_args()

    treebank_file = args.treebank
    grammar_file = args.grammar

    start = time()

    print("Extracting grammar from " + treebank_file + " ...", file=stderr)
    extractor = GrammarExtractor()

    extractor.learn_from_treebank(
        [json.loads(s.strip()) for s in open(treebank_file)]
    )

    print("Saving grammar to " + grammar_file + " ...", file=stderr)
    with open(grammar_file, "w") as f:
        for line in extractor.save_model():
            f.write(line)

    print("Time: %.2fs\n" % (time() - start), file=stderr)


if __name__ == '__main__':
    main()