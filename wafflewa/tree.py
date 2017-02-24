
class Node(object):
    def __init__(self, letter, terminal=False):
        self.letter = letter
        self.terminal = terminal
        self.kids = None # dict()  # dict of Nodes  (for now, we'll just blow it out, see what happens)

def add(root, word):
    n = root
    for letter in word:
        if not n.kids:
            n.kids = dict()
        if letter not in n.kids:
            n.kids[letter] = Node(letter)
        n = n.kids[letter]
    n.terminal = True


def build_tree(file_name=None):
    if not file_name:
        from os import path
        file_name = path.join(path.dirname(path.abspath(__file__)), 'enable1-wwf-v4.0-wordlist.txt')
    root = Node('')
    with open(file_name, 'r') as f:
        for line in f:
            word = line.strip()
            if word:
                add(root, word)
    return root


def add2(root, word):
    """OLD: add using lists instead of dict, this turned out to be slightly slower"""
    n = root
    for letter in word:
        if not n.kids:
            next_kid = Node(letter)
            n.kids = [next_kid]
        else:
            next_kid = None
            for kid in n.kids:
                if letter == kid.letter:
                    next_kid = kid
                    break
            if not next_kid:
                next_kid  = Node(letter)
                n.kids.append(next_kid)
        n = next_kid
    n.terminal = True


def dfs(node, word):
    """full traversal, sanity check"""
    count = 0
    if node.terminal:
        count += 1
        #print word + node.letter
    if node.kids:
        #keys = sorted(node.kids.keys())
        # for k in keys:
        #     dfs(node.kids[k], word + node.letter)
        for n in node.kids.values():
            dfs(n, word + node.letter)
    return count



