class Space(object):
    def __init__(self, mult_letter=1, mult_word=1, display=None):
        #self.points = points
        self.tile = None
        self._mult_letter = mult_letter
        self._mult_word = mult_word
        self._display = display
        self._r = None
        self._c = None

    def attach_to_board(self, board, r, c):
        self._board = board
        self._r = r
        self._c = c

    @property
    def r(self):
        return self._r

    def c(self):
        return self._c

    def board(self):
        return self._board

    def is_empty(self):
        return self.tile is None

    def display(self):
        return self._display if self.is_empty() else self.tile.display()

    # """
    # . - empty (boring)
    # 3 - empty triple letter
    # 2 - empty double letter
    # # - empty triple word
    # @ - empty double word
    # lowercase = blank
    # uppercase = letter
    # """
    #
    # EMPTY = '.'
    # EMPTY_TRIPLE_LETTER = '3'
    # EMPTY_DOUBLE_LETTER = '2'
    # EMPTY_TRIPLE_WORD = ''
    #
    # @property
    # def mult_letter(self):
    #     if self.is_empty():
    #         return self._mult_letter
    #     else:
    #         return 1
    #
    # @property
    # def mult_word(self):
    #     if self.is_empty():
    #         return self._mult_word
    #     else:
    #         return 1

# e = empty = Space(display='.')
# t = triple_letter = Space(mult_letter=3, display='3')
# d = double_letter = Space(mult_letter=2, display='2')
# T = triple_word = Space(mult_word=3, display='#')
# D = double_word = Space(mult_word=2, display='@')

