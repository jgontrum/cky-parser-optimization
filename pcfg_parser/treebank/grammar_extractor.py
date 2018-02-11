import json
from collections import Counter, defaultdict

"""
Base code copied from given starter code.
-> http://stp.lingfil.uu.se/~sara/kurser/parsing18/pcfg_parsing.html
"""


class GrammarExtractor(object):

    def __init__(self, rare_words=5):
        self.RARE_WORD_COUNT = rare_words
        self.well_known_words = set()
        self.q1 = defaultdict(float)
        self.q2 = defaultdict(float)
        self.q3 = defaultdict(float)

    def norm_word(self, word):
        return word if word in self.well_known_words else "_RARE_"  # word_class(word)

    def learn_from_treebank(self, treebank):
        self.sym_count = Counter()
        self.unary_count = Counter()
        self.binary_count = Counter()
        self.words_count = Counter()

        for s in treebank:
            self.count(s)

        # Words
        for word, count in self.words_count.items():
            if count >= self.RARE_WORD_COUNT:
                self.well_known_words.add(word)

        # Normalise the unary rules count
        norm = Counter()
        for (x, word), count in self.unary_count.items():
            norm[(x, self.norm_word(word))] += count
        self.unary_count = norm

        # Q1
        for (x, word), count in self.unary_count.items():
            self.q1[x, word] = self.unary_count[x, word] / self.sym_count[x]

        # Q2
        for (x, y1, y2), count in self.binary_count.items():
            self.q2[x, y1, y2] = self.binary_count[x, y1, y2] / self.sym_count[
                x]

    def count(self, tree):
        # Base case: terminal symbol
        if isinstance(tree, str): return

        # Count the non-terminal symbols
        sym = tree[0]
        self.sym_count[sym] += 1

        if len(tree) == 3:
            # Binary Rule
            y1, y2 = (tree[1][0], tree[2][0])
            self.binary_count[(sym, y1, y2)] += 1

            # Recursively count the children
            self.count(tree[1])
            self.count(tree[2])

        elif len(tree) == 2:
            # Unary Rule
            word = tree[1]
            self.unary_count[(sym, word)] += 1
            self.words_count[word] += 1

    def save_model(self):
        for (x, word), p in self.q1.items():
            yield json.dumps(['Q1', x, word, p]) + '\n'

        for (x, y1, y2), p in self.q2.items():
            yield json.dumps(['Q2', x, y1, y2, p]) + '\n'

        yield json.dumps(['WORDS', list(self.well_known_words)]) + '\n'
