from space import Space
from pieces import Play, Tile
from search import Series


#letter_spaces = dict([(k, Space(letter=k, points=v)) for k, v in point_values.items()])

class Board(object):
    def __init__(self, spaces=None):
        self.spaces = spaces
        if self.spaces:
            for r in xrange(len(self.spaces)):
                for c in xrange(len(self.spaces[r])):
                    self.spaces[r][c].attach_to_board(self, r, c)

    def __repr__(self):
        header = '    ' +  ' '.join([self.get_label(r) for r in xrange(15)])
        line = '  +%s+' % ('-' * (len(header)- 2))
        return "\n".join([header, line] + [" ".join([self.get_label(r), '|'] + [c.display() for c in row] + ['|']) for r, row in enumerate(self.spaces)] + [line])

    def copy(self):
        new_spaces = []
        for r in xrange(len(self.spaces)):
            new_spaces.append([])
            for c in xrange(len(self.spaces[r])):
                new_spaces[r].append(self.spaces[r][c].copy())
        return Board(spaces=new_spaces)

    def get_row_series(self, search, r):
        s = []
        crosswords = []
        for c in xrange(len(self.spaces[r])):
            s.append(self.spaces[r][c].display())
            up = r - 1
            pre = ''
            while up >= 0:
                space = self.spaces[up][c]
                if not space.is_empty():
                    pre = space.display() + pre
                else:
                    break
                up -= 1
            down = r + 1
            post = ''
            bottom = len(self.spaces[r])
            while down < bottom:
                space = self.spaces[down][c]
                if not space.is_empty():
                    post = post + space.display()
                else:
                    break
                down += 1

            crosswords.append((pre, post))

        return Series(search, s, crosswords)

    @staticmethod
    def create_board_from_text(text, special_spaces, tile_source=None):
        # start with made board, add overlay
        board = Board([])
        rows = [line for line in text.splitlines() if line.strip()]
        #print "rows=%s" % rows
        for r, raw_row in enumerate(rows):
            #print "r=%s" % r
            row = raw_row.replace(' ', '')
            board.spaces.append([])
            for c, char in enumerate(row):
                if char.isalpha():
                    if not tile_source:
                        raise RuntimeError("Encountered some letters, need a tile source to create this board properly; tile_source is None")
                    space = Space()
                    space.tile = tile_source.remove(char.lower())
                else:
                    space = special_spaces[char]()
                board.spaces[r].append(space)
                space.attach_to_board(board, r, c)

        return board

    def overlay_letters(self, board_text, tile_source, force=False):
        if not self.spaces:
            raise RuntimeError("Cannot overlay letter because this board doesn't have any spaces.")
        rows = [line for line in board_text.splitlines() if line.strip()]
        #print "rows=%s" % rows
        for r, raw_row in enumerate(rows):
            #print "r=%s" % r
            row = raw_row.replace(' ', '')
            for c, char in enumerate(row):
                space = self.spaces[r][c]
                if char.isalpha():
                    if not tile_source:
                        raise RuntimeError("Encountered some letters, need a tile source to create this board properly; tile_source is None")
                    tile = tile_source.remove(char.lower())
                    if not force and not space.is_empty():
                        raise RuntimeError("Space %s, %s is not empty: %s" % (r, c, space.display()))
                    space.tile = tile
                elif char != '`':
                    raise ValueError("Unrecognized character in board text: %s" % char)

    # def place_tile(self, r, c, tile):
    #     print str(self)
    #     print "placing %s at (%s,%s)" % (tile.display(), r, c)
    #     s = self.spaces[r][c]
    #     if not s.is_empty():
    #         raise RuntimeError('Space (%s, %s) already holds a tile, %s' % (r, c, s.display()))
    #     s.tile = tile


    #def add_word(self, r, c, word, tile_source, vertical=False):

    # def try_word(self, r, c, word, tile_source, vertical=False):
    #     word = word.lower()
    #     mult_word = 1
    #     score = 0
    #     play = Play(vertical)
    #     try:
    #         for letter in word:
    #             space = self.spaces[r][c]
    #             if space.is_empty():
    #                 # Add tile
    #                 tile = tile_source.remove(letter)
    #                 play.stage(tile, space)
    #                 mult_word *= space.mult_word
    #                 letter_score =  space.mult_letter * tile.value
    #             else:
    #                 # Verify current space has matching tile
    #                 tile = space.tile
    #                 if tile.letter != letter:
    #                     raise RuntimeError("Word %s does not fit in this position.  Encounter letter '%s' at (%s,%s)" % (word, letter, r, c))
    #             # print "scored %s for %s" % (letter_score, letter)
    #             score += letter_score
    #             self.spaces[r][c] = letter_spaces[letter]
    #             if vertical:
    #                 r += 1
    #             else:
    #                 c += 1
    #     except IndexError as e:
    #         # roll back...
    #         for tile in hand.dump():
    #             tile_source.add(tile)
    #
    #         raise ValueError("Word %s does not fit in this space starting at (%s,%s), going %s" %
    #                          (word, r, c, 'vertically' if vertical else 'horizontally'))
    #
    #     return score * mult_word

    def get_label(self, index):
        if index < 0 or index > 15:
            raise ValueError("Index must be between 0 and 0xF, got %s" % index)
        return hex(index)[-1].upper()

    # def check_space(self, r, c):
    #     try:
    #         return isinstance(self.spaces[r][c], Space)



# board = Board()
#
# if __name__ == '__main__':
#     # print repr(board)
#     # print "=" * 79
#
#     score = board.add_word(3, 3, 'Briton')
#     print "Scored %s points for Briton" % score
#     score = board.add_word(0, 3, 'zoob', vertical=True)
#     print "Scored %s points for zoob" % score
#     print repr(board)
#
#     print "Scored %s points" % score



