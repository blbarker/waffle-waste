
class Node(object):
    def __init__(self, letter, terminal=False):
        self.letter = letter
        self.terminal = terminal
        self.kids = None  # dict of Nodes


def build_tree(file_name=None):
    """Builds a tree of Nodes using words from the given file, expects one word per line"""
    if not file_name:
        from os import path
        file_name = path.join(path.dirname(path.abspath(__file__)), 'enable1-wwf-v4.0-wordlist.txt')
    root = Node('')
    with open(file_name, 'r') as f:
        for line in f:
            word = line.strip()
            if word:
                add_word(root, word)
    return root


def add_word(root_node, word):
    """Add word to the tree"""
    # Also tried an implementation using lists instead of dict, which turned out to be slightly slower
    n = root_node
    word = word.upper()
    for letter in word:
        if not n.kids:
            n.kids = dict()
        if letter not in n.kids:
            n.kids[letter] = Node(letter)
        n = n.kids[letter]
    n.terminal = True


def _dfs(node, word):
    """depth-first search, full traversal (recursive), used for sanity check"""
    count = 0
    if node.terminal:
        count += 1
        # print word + node.letter
    if node.kids:
        for n in node.kids.values():
            _dfs(n, word + node.letter)
    return count



