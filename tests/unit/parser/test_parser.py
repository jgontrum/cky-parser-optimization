from pcfg_parser.parser.parser import Parser
from pcfg_parser.parser.pcfg import PCFG


def test_parser():
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

    parser = Parser(pcfg)

    assert parser.parse("Peter sees a squirrel") == [
        'S', [
            'NP', 'Peter'],
        ['VP', ['V', 'sees'], ['NP', ['Det', 'a'], ['N', 'squirrel']]]]