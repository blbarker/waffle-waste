from dictionary import build_tree
tree = build_tree()

from search import Search

s = Search(tree)

tell = s.tell

del build_tree, tree, Search, s