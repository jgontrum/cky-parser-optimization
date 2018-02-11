import argparse
import json
from multiprocessing.pool import Pool
from sys import stderr, stdin
from time import time

from pcfg_parser.parser.parser import Parser
from pcfg_parser.parser.pcfg import PCFG


def parse(data):
    sentence_id, sentence, parser = data
    tree = parser.parse(sentence)
    print(f"Finished {sentence_id}.", file=stderr)
    return json.dumps(tree)


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--grammar", help="Path to grammar file.",
                        type=str, required=True)
    parser.add_argument("--threads", help="Number of threads to run on.",
                        type=int, required=False, default=4)
    args = parser.parse_args()

    start = time()
    grammar_file = args.grammar
    threads = args.threads

    print("Loading grammar from " + grammar_file + " ...", file=stderr)

    pcfg = PCFG()
    pcfg.load_model(grammar_file)
    parser = Parser(pcfg)

    print("Parsing sentences ...", file=stderr)
    sentences = [sentence.strip() for sentence in stdin]

    print(f"Received {len(sentences)} sentences...", file=stderr)

    input = [
        (i, sentence, parser) for i, sentence in enumerate(sentences)
    ]

    with Pool(processes=threads) as pool:
        print(f"Pool initialized, start parsing now.", file=stderr)
        output = pool.map(parse, input)
        print("Time: (%.2f)s    \n" % (time() - start), file=stderr)

        for sentence in output:
            print(sentence)

        pool.close()
        pool.join()


if __name__ == "__main__":
    main()
