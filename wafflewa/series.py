class Series(object):
    """
    Represents a row or column on the board, along with its crosses

    A cross is the line of adjacent letters which are perpendicular to a particular space in the series.  It
    is a tuple of two strings (pre, post) in between which a letter is placed and the whole judged as a word.
    The cross can be thought of as the letters above and below a space in a row, or the letters left and right
    of a space in a column.

    ('', '') means there are no crossing letters to be concerned with
    """

    def __init__(self, line, crosses=None):
        if crosses and len(line) != len(crosses):
            raise ValueError("The number of crosses provided (%s) must equal the length of the line '%s' (%s)" %
                             (len(crosses), len(line), line))
        self.line = line
        self.crosses = crosses or []

    def __repr__(self):
        return "%s  [%s]" % (self.line, (",".join([str(cw) for cw in self.crosses]) if self.crosses else ''))

    def get_space(self, index):
        """returns the space char in the Series line for the given index"""
        try:
            return self.line[index]
        except IndexError:
            return None

    def get_cross(self, index):
        """returns the cross tuple in the Series line for the given index"""
        try:
            return self.crosses[index]
        except IndexError:
            return '', ''

    def copy(self):
        return Series(self.line, crosses=self.crosses)

    def word_can_start_and_end(self, word, index):
        """returns whether a word can end in the current position"""
        start_index = index - len(word)
        can_start = (start_index == 0 or
                     (start_index > 0
                      and not self.line[start_index-1].isalpha()))
        can_end = (index >= len(self.line) or (not self.line[index].isalpha()))
        return can_start and can_end


