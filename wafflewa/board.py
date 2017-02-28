from series import Series


class Board(object):

    def __init__(self, source, special_spaces):
        if isinstance(source, basestring):
            source = self._parse_string(source, special_spaces)
        self.rows = source
        self.special_spaces = special_spaces

    def __repr__(self):
        header = '    ' + ' '.join([self._get_rc_label(r) for r in xrange(self.num_cols)])
        line = '  +%s+' % ('-' * (len(header) - 2))
        return "\n".join([header, line] + [" ".join([self._get_rc_label(r), '|'] + [c for c in row] + ['|'])
                                           for r, row in enumerate(self.rows)] + [line])

    def copy(self):
        new_rows = [list(row) for row in self.rows]
        return Board(new_rows, self.special_spaces)

    @property
    def num_rows(self):
        return len(self.rows)

    @property
    def num_cols(self):
        return max([len(row) for row in self.rows])

    def get_row_series(self, row_index):
        """Creates a Series object for the given row index"""
        r = row_index
        s = []
        crosswords = []
        for c in xrange(len(self.rows[r])):
            s.append(self.rows[r][c])
            up = r - 1
            pre = ''
            while up >= 0:
                space = self.rows[up][c]
                if self.char_means_empty(space):
                    break
                else:
                    pre = space + pre
                up -= 1
            down = r + 1
            post = ''
            bottom = len(self.rows[r])
            while down < bottom:
                space = self.rows[down][c]
                if self.char_means_empty(space):
                    break
                else:
                    post = post + space
                down += 1

            crosswords.append((pre, post))

        return Series(s, crosswords)

    @staticmethod
    def _parse_string(text, special_spaces):
        """
        Parses text and returns rows as a list of space strings

        :param text: string describing board, each line is a row (the repr format with rc labels is also accepted)
        :param special_spaces: dictionary of special space characters and how they affect the score
        :return: list of str
        """

        rows = []
        for raw_line in text.splitlines():
            line = raw_line.replace(' ', '')
            line = line.strip()
            if line:
                # ignore repr markup
                if line.startswith('01') or line.startswith('+-'):
                    continue
                if line[1] == '|':
                    line = line[1:]
                line = line.strip('|')

                rows.append(line.upper())

        # Validate rows are OK
        num_rows = len(rows)
        for r, row in enumerate(rows):
            if num_rows != len(rows):
                raise ValueError("Not a square board! row %s doesn't have %s columns" % (row, num_rows))
            for c, char in enumerate(row):
                if not char.isalpha() and char not in special_spaces:
                    raise ValueError("Unrecognized character %s found at (%s,%s)" % (char, r, c))
        return rows

    @staticmethod
    def char_means_empty(space_char):
        """Indicates whether the given space character means the space is empty (i.e. no tile)"""
        return not space_char.isalpha()

    @staticmethod
    def _get_rc_label(index):
        # todo: raise limit beyond 16
        if index < 0 or index > 15:
            raise ValueError("Index must be between 0 and 0xF, got %s.  Probably means too many rows or columns were defined" % index)
        return hex(index)[-1].upper()

    def transposed(self):
        """Returns a transposed board for vertical searching"""
        copy = self.copy()
        for r in xrange(self.num_rows):
            for c in xrange(self.num_rows):
                copy.rows[r][c] = self.rows[c][r]
        return copy

    def overlay(self, overlay_text, force=False):
        if not self.rows:
            raise RuntimeError("Cannot overlay letter because this board doesn't have any rows.")
        rows = []
        for raw_line in overlay_text.splitlines():
            line = raw_line.replace(' ', '')
            line = line.strip()
            if line:
                # ignore repr markup
                if line.startswith('01') or line.startswith('+-'):
                    continue
                if line[1] == '|':
                    line = line[1:]
                line = line.strip('|').upper()
                new_line_chars = []
                r = len(rows)
                for c, char in enumerate(line):
                    if char.isalpha():
                        if self.rows[r][c].isalpha() and not force:
                            raise RuntimeError("Space %s,%s not empty: %s.  Try force option" % (r, c, self.rows[r][c]))
                        new_line_chars.append(char)
                    elif char == '`':
                        new_line_chars.append(self.rows[r][c])
                    else:
                        raise ValueError("Unrecognized character in overaly text: %s" % char)

                if len(new_line_chars) != len(self.rows[r]):
                    raise RuntimeError("Not enough columns in row %s to overlay properly" % r)
                rows.append(''.join(new_line_chars))

        if len(rows) != len(self.rows):
            raise RuntimeError("Not enough rows to overlay properly")

        self.rows = rows

    def play(self, word, r=None, c=None, vertical=None, force=False):
        if isinstance(word, tuple):
            vertical = word[4] == 'v'
            c = word[3]
            r = word[2]
            word = word[0]
        else:
            if r is None or c is None or vertical is None:
                raise RuntimeError("Bad arguments given to play()")
            if vertical == 'h':
                vertical = False

        def get_err():
            return RuntimeError("The word '%s' doesn't fit %s at %s,%s" % (word,
                                                                           "vertically" if vertical else "horizontally",
                                                                           r,
                                                                           c))

        def play_row(board, r_index, c_index):
            board_row = ''.join(board.rows[r_index])
            new_row = board_row[:c_index] + word + board_row[c_index + len(word):]

            if len(new_row) != len(board_row):
                raise get_err()

            if not force:
                for i, char in enumerate(board_row):
                    if char.isalpha() and new_row[i] != char:
                        raise get_err()
            return new_row

        if vertical:
            transposed = self.transposed()
            vertical_row = play_row(transposed, c, r)
            transposed.rows[c] = vertical_row
            self.rows = transposed.transposed().rows
        else:
            self.rows[r] = play_row(self, r, c)

        self.validate()

    def validate(self):
        """Makes sure all the words are connected and that the tile bag is honored"""
        rows = self.copy().rows

        # look for first letter
        start_r, start_c = None, None
        for r, row in enumerate(rows):
            for c, char in enumerate(row):
                if char.isalpha():
                    start_r, start_c = r, c
                    break
            if start_r is not None:
                break

        if start_r is None:
            return True  # Empty Board!

        NOWHERE = -1
        LEFT = 0
        RIGHT = 1
        UP = 2
        DOWN = 3
        MARKER = '~'

        def walker(rows, enter_from, r, c):
            if rows[r][c].isalpha():
                rows[r][c] = MARKER
                # add letter to tile bags...
            else:
                return  # not a letter

            if enter_from != LEFT and c > 0:
                walker(rows, RIGHT, r, c - 1)
            if enter_from != RIGHT and c < len(rows[r])-1:
                walker(rows, LEFT, r, c + 1)
            if enter_from != UP and r > 0:
                walker(rows, DOWN, r - 1, c)
            if enter_from != DOWN and r < len(rows)-1:
                walker(rows, UP, r + 1, c)

        # start traversal
        walker(rows, NOWHERE, start_r, start_c)

        # start over a see if any letter remain
        for r, row in enumerate(rows):
            for c, char in enumerate(row):
                if char.isalpha():
                    raise RuntimeError("Board is not fully connected.  Look at '%s' at position %s, %s" % (char, r, c))

        # Secondly - tile counts are appropriate
        # todo: count the letter
