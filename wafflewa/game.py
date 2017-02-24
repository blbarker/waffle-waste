from board import Board
from pieces import TileBag, Rack
from search import Search


def create_wwf_game(rack_str):
    import wwf
    tree = wwf.build_tree()
    board = Board.create_board_from_text(wwf.new_board_string, wwf.special_spaces)
    return Game(tree, board, wwf.tile_tuples, wwf.ScoreFactory, wwf.rack_capacity, rack_str)


def create_wwf_test_board(text):
    import wwf
    bag = TileBag.create(wwf.tile_tuples)
    board = Board.create_board_from_text(wwf.new_board_string, wwf.special_spaces)
    #print "board A ->\n%s" % board
    board.overlay_letters(text, bag)
    return board

def create_wwf_search():
    import wwf
    return Search(wwf.build_tree(), wwf.ScoreFactory)

class Game(object):

    def __init__(self, tree, board, tile_tuples, score_factory, rack_capacity, rack_str):
        self.tree = tree
        self.board = board
        self.bag = TileBag.create(tile_tuples)
        self.score_factory = score_factory
        self.letter_values = {}
        for letter, value, count in tile_tuples:
            self.letter_values[letter] = value
        if len(rack_str) != rack_capacity:
            raise ValueError("rack_str must be %s letters long" % rack_capacity)
        self.rack = Rack(rack_capacity)
        self.update_rack(rack_str)
        self.tree_search = Search(self.tree, self.score_factory)


    def update_rack(self, letters):
        must_find_count = len(self.rack.tiles)
        from_rack = []
        fresh_from_bag = []
        try:
            for letter in letters:
                tile = self.rack.remove(letter, allow_missing=True)
                if tile:
                    from_rack.append(tile)
                else:
                    tile = self.bag.remove(letter)
                    fresh_from_bag.append(tile)

            if len(from_rack) != must_find_count:
                raise RuntimeError("update rack problem: needed to find %s in the rack but found %s" % (must_find_count, len(from_rack)))
        except Exception as e:
            # roll back
            for tile in from_rack:
                self.rack.add(tile)
            self.bag.add(fresh_from_bag)
            raise e
        else:
            # commit
            for tile in from_rack + fresh_from_bag:
                self.rack.add(tile)

    def __repr__(self):
        return self._get_show_str()

    def _get_show_str(self):
        b = str(self.board)
        r = self.rack._get_show_str()
        return "%s\n\n%s" % (b, r)

    def bag_details(self):
        self.bag.show()

    def tell(self, letters, series=None, top_k=10):
        return self.tree_search.tell(letters, series, top_k=top_k)

    def tell2(self, letters, series, top_k=10, threshold=5):
        return self.tree_search.tell2(letters, series, top_k, threshold)

    def tell3(self, letters, series, top_k=10, threshold=5):
        return self.tree_search.tell3(letters, series, top_k, threshold)

    def make_series(self, string, crosswords=None, index=0):
        from search import Series
        return Series(self.tree_search, string, crosswords=crosswords, index=index)

    def waste(self, k=3):
        #
        #if self.board.
        #start here... the good wasting part...
        pass

    def move(self, move_id):
        pass

    def rack(self, letters):
        pass

    def opponent(self, word, r, c, vertical):
        pass

    def edit_board(self, word, r, c, vertical):
        """edit the board manually"""
        pass


    def edit_bag(self, contents):
        """hopefully you won't need this?"""
        pass