from points import point_values

class Space(object):
    def __init__(self, letter='', points=0, mult_letter=1, mult_word=1, display=None):
        self.letter = letter
        self.points = points
        self.mult_letter = mult_letter
        self.mult_word = mult_word
        self._display = display

    @property
    def display(self):
        return self._display if self._display else self.letter.upper()

    """
    . - empty (boring)
    3 - empty triple letter
    2 - empty double letter
    # - empty triple word
    * - empty double word
    lowercase = blank
    uppercase = letter
    """

e = empty = Space(display='.')
t = triple_letter = Space(mult_letter = 3, display='3')
d = double_letter = Space(mult_letter = 2, display='2')
T = triple_word = Space(mult_word = 3, display='#')
D = double_word = Space(mult_word = 2, display='@')

letter_spaces = dict([(k, Space(letter=k, points=v)) for k, v in point_values.items()])

class Board(object):
    def __init__(self, board_type='wwf'):
        if board_type == 'wwf':
            self.spaces = self._get_new_wwf_board()
        else:
            raise RuntimeError("No support for board type '%s'" % board_type)

    def _get_new_wwf_board(self):
        return [[e, e, e, T, e, e, t, e, t, e, e, T, e, e, e],
            [e, e, d, e, e, D, e, e, e, D, e, e, d, e, e],
            [e, d, e, e, d, e, e, e, e, e, d, e, e, d, e],
            [T, e, e, t, e, e, e, D, e, e, e, t, e, e, T],
            [e, e, d, e, e, e, d, e, d, e, e, e, d, e, e],
            [e, D, e, e, e, t, e, e, e, t, e, e, e, D, e],
            [t, e, e, e, d, e, e, e, e, e, d, e, e, e, t],
            [e, e, e, D, e, e, e, e, e, e, e, D, e, e, e],
            [t, e, e, e, d, e, e, e, e, e, d, e, e, e, t],
            [e, D, e, e, e, t, e, e, e, t, e, e, e, D, e],
            [e, e, d, e, e, e, d, e, d, e, e, e, d, e, e],
            [T, e, e, t, e, e, e, D, e, e, e, t, e, e, T],
            [e, d, e, e, d, e, e, e, e, e, d, e, e, d, e],
            [e, e, d, e, e, D, e, e, e, D, e, e, d, e, e],
            [e, e, e, T, e, e, t, e, t, e, e, T, e, e, e]]

    def __repr__(self):
        header = '    ' +  ' '.join([self.get_label(r) for r in xrange(15)])
        line = '  +%s+' % ('-' * (len(header)- 2))
        return "\n".join([header, line] + [" ".join([self.get_label(r), '|'] + [c.display for c in row] + ['|']) for r, row in enumerate(self.spaces)] + [line])

    def add_word(self, r, c, word, vertical=False):
        word = word.lower()
        mult_word = 1
        score = 0
        try:
            for letter in word:
                mult_word *= self.spaces[r][c].mult_word
                letter_score =  self.spaces[r][c].mult_letter * point_values[letter]
                # print "scored %s for %s" % (letter_score, letter)
                score += letter_score
                self.spaces[r][c] = letter_spaces[letter]
                if vertical:
                    r += 1
                else:
                    c += 1
        except IndexError as e:
            raise ValueError("Word %s does not fit in this space starting at (%s,%s), going %s" %
                             (word, r, c, 'vertically' if vertical else 'horizontally'))

        return score * mult_word

    def get_label(self, index):
        if index < 0 or index > 15:
            raise ValueError("Index must be between 0 and 0xF, got %s" % index)
        return hex(index)[-1].upper()



board = Board()

if __name__ == '__main__':
    # print repr(board)
    # print "=" * 79

    score = board.add_word(3, 3, 'Briton')
    print "Scored %s points for Briton" % score
    score = board.add_word(0, 3, 'zoob', vertical=True)
    print "Scored %s points for zoob" % score
    print repr(board)

    print "Scored %s points" % score



