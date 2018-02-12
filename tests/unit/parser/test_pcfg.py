import math

import numpy as np

from pcfg_parser.parser.pcfg import PCFG


def test_construct_pcfg():
    grammar = [
        '["Q1", "NP", "Peter", 0.5]',
        '["Q1", "V", "sees", 1.0]',
        '["Q1", "Det", "a", 1.0]',
        '["Q1", "N", "squirrel", 1.0]',
        '["Q2", "S", "NP", "VP", 1.0]',
        '["Q2", "VP", "V", "NP", 1.0]',
        '["Q2", "NP", "Det", "N", 0.5]',
        '["WORDS", ["Peter", "a", "sees", "squirrel"]]'
    ]

    pcfg = PCFG()
    pcfg.load_model(grammar)

    lookup = pcfg.get_lhs(
        pcfg.get_id_for_word("NP"),
        pcfg.get_id_for_word("VP")
    )

    item = [
        pcfg.get_id_for_word("S"),
        pcfg.get_id_for_word("NP"),
        pcfg.get_id_for_word("VP"),
        math.log(1.0)
    ]
    assert len(lookup) == 1
    assert lookup[0][0] == item[0]
    assert lookup[0][1] == item[1]
    assert lookup[0][2] == item[2]
    assert lookup[0][3] == item[3]

