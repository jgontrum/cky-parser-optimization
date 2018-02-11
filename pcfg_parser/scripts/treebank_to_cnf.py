from sys import stdin

from pcfg_parser.treebank.tree import Tree


def main():
    for tree in stdin:
        t = Tree(text=tree.strip())
        print(Tree(t.to_cnf()).save().strip())


if __name__ == '__main__':
    main()