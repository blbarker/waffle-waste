from board import Board
from search import Search


def create_wwf_game(text=None):
    import wwf
    tree = wwf.build_tree()
    board = Board(text or wwf.new_board_string, wwf.special_spaces)
    return Game(tree, board, wwf.tile_tuples, wwf.ScoreFactory)


def create_wwf_board(text):
    import wwf
    from board import Board
    board = Board(text, wwf.special_spaces)
    return board


def create_wwf_search():
    import wwf
    return Search(wwf.build_tree(), wwf.ScoreFactory)


class Game(object):

    def __init__(self, tree, board, tile_tuples, score_factory):
        self.tree = tree
        self.board = board
        self.score_factory = score_factory
        self.letter_values = {}
        for letter, value, count in tile_tuples:
            self.letter_values[letter] = value
        self.tree_search = Search(self.tree, self.score_factory)

    def get_best(self, letters, top_k=10, threshold=5):
        return self.tree_search.get_candidates(letters, self.board, top_k, threshold)

    def is_word(self, word):
        return self.tree_search.is_word(word.upper())

    def __repr__(self):
        return self._get_show_str()

    def _get_show_str(self):
        return str(self.board)
