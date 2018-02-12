"""
CKY algorithm from the "Natural Language Processing" course by Michael Collins
https://class.coursera.org/nlangp-001/class
"""
from itertools import chain

import numpy as np

from pcfg_parser.parser.tokenizer import PennTreebankTokenizer


class ChartItem(object):
    class Backpointer(object):
        def __init__(self, i, j, symbol):
            self.i = i
            self.j = j
            self.symbol = symbol

    def __init__(self, symbol, probability, bp_1=None, bp_2=None,
                 terminal=None):
        self.symbol = symbol
        self.probability = probability

        self.backpointers = (
            ChartItem.Backpointer(bp_1[0], bp_1[1], bp_1[2]),
            ChartItem.Backpointer(bp_2[0], bp_2[1], bp_2[2])
        ) if bp_1 else None

        self.terminal = terminal

    def __repr__(self):
        return f"[{self.symbol},{self.probability:0.4f}]"


class Parser:
    def __init__(self, pcfg):
        self.pcfg = pcfg
        self.tokenizer = PennTreebankTokenizer()

    def parse(self, sentence):
        words = self.tokenizer.tokenize(sentence)
        norm_words = []
        for word in words:  # rare words normalization + keep word
            norm_words.append((self.pcfg.norm_word(word), word))
        tree = self.cky(self.pcfg, norm_words)
        tree[0] = tree[0].split("|")[0]

        return tree

    def backtrace(self, item, chart, pcfg):
        if item.terminal:
            assert item.backpointers is None
            return [
                pcfg.get_word_for_id(item.symbol),
                item.terminal
            ]

        rhs_1, rhs_2 = item.backpointers

        return [
            pcfg.get_word_for_id(item.symbol),
            self.backtrace(
                chart[rhs_1.i][rhs_1.j][rhs_1.symbol],
                chart, pcfg
            ),
            self.backtrace(
                chart[rhs_2.i][rhs_2.j][rhs_2.symbol],
                chart, pcfg
            )
        ]

    def cky(self, pcfg, norm_words):
        # Initialize your charts (for scores and backpointers)
        size = len(norm_words)
        chart = [[{} for _ in range(size)] for _ in range(size)]

        # Code for adding the words to the chart
        for i, (norm, word) in enumerate(norm_words):
            id_ = pcfg.get_id_for_word(norm)
            for lhs, prob in pcfg.get_lhs_for_terminal_rule(id_):
                item = ChartItem(lhs, prob, terminal=word)
                existing_item = chart[i][i].get(lhs)
                if not existing_item or \
                        existing_item.probability < item.probability:
                    chart[i][i][lhs] = item

        # Implementation is based upon J&M
        for j in range(size):
            for i in range(j, -1, -1):
                for k in range(i, j):
                    first_nts = chart[i][k]
                    second_nts = chart[k + 1][j]

                    first_symbols = np.array(list(first_nts.keys()))
                    second_symbols = np.array(list(second_nts.keys()))

                    if not first_symbols.size or not second_symbols.size:
                        continue

                    valid_rows = np.take(
                        pcfg.rhs_to_lhs_id, first_symbols, axis=0)

                    valid_ids = np.take(
                        valid_rows, second_symbols, axis=1).flatten()

                    non_zero = np.nonzero(valid_ids)

                    lhs_ids = valid_ids[non_zero].flatten()

                    if not lhs_ids.size:
                        continue

                    lhs_items = np.take(pcfg.id_to_lhs, lhs_ids, axis=0)

                    for lhs, rhs_1, rhs_2, prob in chain(*lhs_items):
                        rhs_1_cell = first_nts[rhs_1]
                        rhs_2_cell = second_nts[rhs_2]

                        probability = rhs_1_cell.probability
                        probability += rhs_2_cell.probability
                        probability += prob

                        existing_item = chart[i][j].get(lhs)
                        if not existing_item \
                                or existing_item.probability < probability:
                            item = ChartItem(lhs, probability,
                                             (i, k, rhs_1),
                                             (k + 1, j, rhs_2))
                            chart[i][j][lhs] = item

        return self.backtrace(chart[0][-1][pcfg.start_symbol], chart, pcfg)

    def print_chart(self, chart):
        print("    |" + "".join([f"{i:^20}|" for i in range(len(chart))]))
        print("".join(["-" for _ in range(5 + len(chart) * 21)]))
        for i, row in enumerate(chart):
            print(f"{i:>2}: |" + "".join(
                ["{0:<20}|".format(str(set(cell.values()))) for cell in row]))
