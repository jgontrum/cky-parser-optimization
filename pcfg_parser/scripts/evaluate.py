import json
import argparse

from pcfg_parser.treebank.eval import ParseEvaluator


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--gold", help="The gold file to evaluate against.",
                        type=str, required=True)

    parser.add_argument("--test", help="The test file to evaluate.",
                        type=str, required=True)
    args = parser.parse_args()

    key_file = args.gold
    prediction_file = args.test

    key_trees = [json.loads(l) for l in open(key_file)]
    predicted_trees = [json.loads(l) for l in open(prediction_file)]
    evaluator = ParseEvaluator()
    evaluator.compute_fscore(key_trees, predicted_trees)
    evaluator.output()
