import json

from pcfg_parser.treebank.grammar_extractor import GrammarExtractor


def test_grammar_extractor():
    treebank = [
        ["S",
         ["NP", "Peter"],
         ["VP", ["V", "sees"], ["NP", ["Det", "a"], ["N", "squirrel"]]]
         ]
    ]

    extractor = GrammarExtractor(rare_words=0)
    extractor.learn_from_treebank(treebank)

    model = [json.loads(l) for l in extractor.save_model()]

    assert ["Q1", "NP", "Peter", 0.5] in model
    assert ["Q1", "V", "sees", 1.0] in model
    assert ["Q1", "V", "sees", 1.0] in model
    assert ["Q1", "Det", "a", 1.0] in model
    assert ["Q1", "N", "squirrel", 1.0] in model
    assert ["Q2", "S", "NP", "VP", 1.0] in model
    assert ["Q2", "VP", "V", "NP", 1.0] in model
    assert ["Q2", "NP", "Det", "N", 0.5] in model

    words = set(list(filter(lambda x: x[0] == "WORDS", model))[0][1])
    assert len(words.difference({"Peter", "sees", "a", "squirrel"})) == 0

    assert len(model) == 8
