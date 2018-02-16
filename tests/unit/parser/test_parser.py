import os

from pcfg_parser.parser.parser import Parser
from pcfg_parser.parser.pcfg import PCFG

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

tree = [
    'S', [
        'NP', 'Peter'],
    ['VP', ['V', 'sees'], ['NP', ['Det', 'a'], ['N', 'squirrel']]]]


def test_parser_matrix():
    os.environ['MATRIXTHRESHOLD'] = "0"
    pcfg = PCFG()
    pcfg.load_model(grammar)

    parser = Parser(pcfg)

    assert parser.parse("Peter sees a squirrel") == tree


def test_parser_intersection():
    os.environ['MATRIXTHRESHOLD'] = "999999999999999999"
    pcfg = PCFG()
    pcfg.load_model(grammar)

    parser = Parser(pcfg)

    assert parser.parse("Peter sees a squirrel") == tree
