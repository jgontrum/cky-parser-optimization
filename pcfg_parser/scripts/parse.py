import argparse
import json
from multiprocessing.pool import Pool
from sys import stderr, stdin
from time import time

from pcfg_parser.parser.parser import Parser
from pcfg_parser.parser.pcfg import PCFG


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

        runtime = 0
        for sentence, t in output:
            runtime = + t
            print(sentence)

        print("Time: (%.2f)s    \n" % runtime, file=stderr)

        pool.close()
        pool.join()


if __name__ == "__main__":
    main()
