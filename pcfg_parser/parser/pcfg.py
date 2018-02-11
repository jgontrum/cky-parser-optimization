# from __future__ import division
import math
from collections import defaultdict
from json import loads

# from stat_parser.word_classes import word_class
import numpy as np
from scipy.sparse import dok_matrix


class PCFG():

    def __init__(self, start_symbol="S"):
        self.word_to_id = {"UNARY": 0}
        self.id_to_word = ["UNARY"]

        self.well_known_words = {}
        self.start_symbol = self.__add_to_signature(start_symbol)

    def norm_word(self, word):
        return word if word in self.well_known_words else "_RARE_"

    def get_lhs(self, rhs_1, rhs_2=0):
        lhs_id = self.rhs_to_lhs_id[rhs_1, rhs_2]
        return self.id_to_lhs[lhs_id - 1]

    def get_id_for_word(self, word):
        return self.word_to_id.get(word)

    def get_word_for_id(self, id_):
        return self.id_to_word[id_]

    def __build_caches(self):
        size = len(self.id_to_word)
        self.rhs_to_lhs_id = dok_matrix((size, size), dtype=np.int32)
        self.first_rhs_to_second_rhs = defaultdict(set)

        for i, (lhs, rhs, prob) in enumerate(self.rule_cache):
            rhs_1 = rhs[0]
            rhs_2 = rhs[1] if len(rhs) > 1 else 0

            lhs_id = self.rhs_to_lhs_cache[tuple(rhs)]

            self.rhs_to_lhs_id[rhs_1, rhs_2] = lhs_id
            self.first_rhs_to_second_rhs[rhs_1].add(rhs_2)

        self.rhs_to_lhs_id = self.rhs_to_lhs_id.tocsr()
        self.id_to_lhs = np.asarray(self.id_to_lhs)

        self.rule_cache.clear()

    def __add_to_signature(self, word):
        if word in self.word_to_id:
            return self.word_to_id.get(word)

        new_id = len(self.id_to_word)
        self.id_to_word.append(word)
        self.word_to_id[word] = new_id
        return new_id

    def load_model(self, path):
        self.rule_cache = []
        self.id_to_lhs = []
        self.rhs_to_lhs_cache = {}

        with open(path) as model:
            for line in model:
                data = loads(line)

                if data[0] == 'WORDS':
                    self.well_known_words = data[1]
                    for word in self.well_known_words:
                        self.__add_to_signature(word)
                    continue

                lhs_raw = data[1]
                rhs_raw = data[2:-1]
                prob = data[-1]

                lhs = self.__add_to_signature(lhs_raw)
                rhs = [self.__add_to_signature(sym) for sym in rhs_raw]

                item = (lhs, math.log(prob))

                lhs_id = self.rhs_to_lhs_cache.get(tuple(rhs))

                if lhs_id is None:
                    self.id_to_lhs.append([item])
                    lhs_id = len(self.id_to_lhs)
                    self.rhs_to_lhs_cache[tuple(rhs)] = lhs_id
                else:
                    self.id_to_lhs[lhs_id - 1].append(item)

                self.rule_cache.append((lhs, rhs, prob))

        self.__add_to_signature("_RARE_")
        self.__build_caches()
