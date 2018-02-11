import json

import nltk.tree


class Tree(object):

    def __init__(self, structure: list = None, text: str = None):
        """
        Constructs a Tree object either from a given list structure
        or a string encoding the tree as a list.
        :param structure: List based tree structure
        :param text: Like structure, but encoded as a string.
        """
        if text:
            self.load(text)
        else:
            self.structure = structure if structure is not None else []

    def load(self, text: str):
        self.structure = json.loads(text)

    def save(self) -> str:
        return json.dumps(self.structure)

    def visualize(self):
        self.to_nltk_tree().pretty_print()

    def to_nltk_tree(self) -> nltk.tree.Tree:
        as_str = self.save()
        # Transform the string representation of the tree
        # to the string representation of an NLTK tree
        as_str = as_str.replace("[", "(").replace("]", ")")
        as_str = as_str.replace(', ', " ").replace('"', "")
        return nltk.tree.Tree.fromstring(as_str)

    def __repr__(self) -> str:
        return self.save()

    def is_cnf(self, tree=None) -> bool:
        """
        Returns true, if the tree is in CNF.
        Adapted from starter code.
        """
        if tree is None:
            tree = self.structure
        n = len(tree)
        if n == 2:
            return isinstance(tree[1], str)
        elif n == 3:
            return self.is_cnf(tree[1]) and self.is_cnf(tree[2])
        else:
            return False

    def to_cnf(self) -> list:
        structure = self.structure

        if (type(structure) is str or
                (len(structure) == 2 and type(structure[1]) is str)):
            # Base case: Root symbol like "NP" or leaves
            return structure

        while len(structure) == 2 and type(structure[1]) is list:
            # Remove unary rules
            new_node = f"{structure[0]}&{structure[1][0]}"
            structure = [new_node] + structure[1][1:]

        if len(structure) > 3:
            # Binarize
            part_one = structure[:2]
            part_two = structure[2:]
            new_node = f"{part_one[0]}|{part_one[1][0]}"
            structure = part_one + [[new_node] + part_two]

        # Recursion: Convert all subtrees to CNF
        structure = [Tree(l).to_cnf() for l in structure]

        return structure
