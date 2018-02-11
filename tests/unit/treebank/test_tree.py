from pcfg_parser.treebank.tree import Tree

t = '["S", ["PP", ["IN", "Among"], ["NP", ["NP", ["CD", "33"], ' \
    '["NNS", "men"]], ["SBAR", ["WHNP", ["WP", "who"]], ' \
    '["S", ["VP", ["VBD", "worked"], ["ADVP", ["RB", "closely"]], ' \
    '["PP", ["IN", "with"], ["NP", ["DT", "the"], ' \
    '["NN", "substance"]]]]]]]], [",", ","], ["NP", ["NP", ' \
    '["CD", "28"]]], ["VP", ["VBP", "have"], ["VP", ["VBN", "died"], ' \
    '[":", "--"], ["NP", ["QP", ["JJ", "more"], ["IN", "than"], ' \
    '["CD", "three"], ["NNS", "times"]], ["DT", "the"], ' \
    '["VBN", "expected"], ["NN", "number"]]]], [".", "."]]'


def test_tree_construction():
    tree = Tree(text=t)

    assert tree.structure == [
        'S',
        ['PP', ['IN', 'Among'],
         ['NP', ['NP', ['CD', '33'],
                 ['NNS', 'men']],
          ['SBAR', ['WHNP', ['WP', 'who']],
           ['S', ['VP', ['VBD', 'worked'],
                  ['ADVP', ['RB', 'closely']],
                  ['PP', ['IN', 'with'],
                   ['NP', ['DT', 'the'],
                    ['NN', 'substance']]]]]]]],
        [',', ','],
        ['NP', ['NP', ['CD', '28']]],
        ['VP', ['VBP', 'have'],
         ['VP', ['VBN', 'died'], [':', '--'],
          ['NP', ['QP', ['JJ', 'more'], ['IN', 'than'], ['CD', 'three'],
                  ['NNS', 'times']], ['DT', 'the'], ['VBN', 'expected'],
           ['NN', 'number']]]], ['.', '.']]


def test_tree_to_cnf():
    tree = Tree(text=t)

    assert Tree(tree.to_cnf()).is_cnf()
