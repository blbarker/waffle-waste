from series import Series


class Board(object):

    def __init__(self, source, special_spaces):
        if isinstance(source, basestring):
            source = self._parse_string(source, special_spaces)
        self.rows = source
        self.special_spaces = special_spaces

    def __repr__(self):
        header = '    ' +  ' '.join([self._get_rc_label(r) for r in xrange(self.num_cols)])
        line = '  +%s+' % ('-' * (len(header)- 2))
        return "\n".join([header, line] + [" ".join([self._get_rc_label(r), '|'] + [c for c in row] + ['|']) for r, row in enumerate(self.rows)] + [line])

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

    # def overlay_letters(self, board_text, tile_source, force=False):
    #     if not self.spaces:
    #         raise RuntimeError("Cannot overlay letter because this board doesn't have any spaces.")
    #     rows = [line for line in board_text.splitlines() if line.strip()]
    #     #print "rows=%s" % rows
    #     for r, raw_row in enumerate(rows):
    #         #print "r=%s" % r
    #         row = raw_row.replace(' ', '')
    #         for c, char in enumerate(row):
    #             space = self.spaces[r][c]
    #             if char.isalpha():
    #                 if not tile_source:
    #                     raise RuntimeError("Encountered some letters, need a tile source to create this board properly; tile_source is None")
    #                 tile = tile_source.remove(char)
    #                 if not force and not space.is_empty():
    #                     raise RuntimeError("Space %s, %s is not empty: %s" % (r, c, space.display()))
    #                 space.tile = tile
    #             elif char != '`':
    #                 raise ValueError("Unrecognized character in board text: %s" % char)
