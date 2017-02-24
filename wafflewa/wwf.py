from space import *

rack_capacity = 7

tile_tuples = [
    ('a', 1, 9),
    ('b', 2, 2),
    ('c', 4, 2),
    ('d', 2, 5),
    ('e', 1, 13),
    ('f', 4, 2),
    ('g', 3, 3),
    ('h', 4, 4),
    ('i', 1, 8),
    ('j', 10, 1),
    ('k', 5, 1),
    ('l', 2, 4),
    ('m', 4, 2),
    ('n', 2, 5),
    ('o', 1, 8),
    ('p', 4, 2),
    ('q', 10, 1),
    ('r', 1, 6),
    ('s', 1, 5),
    ('t', 1, 7),
    ('u', 2, 4),
    ('v', 5, 2),
    ('w', 4, 2),
    ('x', 8, 1),
    ('y', 3, 2),
    ('z', 10, 1),
    (' ', 0, 2)
]


# this next stuff is pretty gross...
DISPLAY_EMPTY = '.'
DISPLAY_TRIPLE_LETTER = '3'
DISPLAY_DOUBLE_LETTER = '2'
DISPLAY_TRIPLE_WORD = '#'
DISPLAY_DOUBLE_WORD = '@'

from collections import namedtuple

SpecialSpace = namedtuple("SpecialSpace", ['display', 'mult_letter', 'mult_word'])

special_spaces = {}

for ss in [
    SpecialSpace(display=DISPLAY_EMPTY, mult_letter=1, mult_word=1),
    SpecialSpace(display=DISPLAY_TRIPLE_LETTER, mult_letter=3, mult_word=1),
    SpecialSpace(display=DISPLAY_DOUBLE_LETTER, mult_letter=2, mult_word=1),
    SpecialSpace(display=DISPLAY_TRIPLE_WORD, mult_letter=1, mult_word=3),
    SpecialSpace(display=DISPLAY_DOUBLE_WORD, mult_letter=1, mult_word=2)]:

    def get_get():
        ml = ss.mult_letter
        mw = ss.mult_word
        d = ss.display

        def get_special_space():
            return Space(mult_letter=ml, mult_word=mw, display=d)

        return get_special_space

    special_spaces[ss.display] = get_get()

# e = empty = Space(display=DISPLAY_EMPTY)
# t = triple_letter = Space(mult_letter=3, display=DISPLAY_TRIPLE_LETTER)
# d = double_letter = Space(mult_letter=2, display=DISPLAY_DOUBLE_LETTER)
# T = triple_word = Space(mult_word=3, display=DISPLAY_TRIPLE_WORD)
# D = double_word = Space(mult_word=2, display=DISPLAY_DOUBLE_WORD)


def get_empty_space():
    return Space(display=DISPLAY_EMPTY)
t = triple_letter = Space(mult_letter=3, display=DISPLAY_TRIPLE_LETTER)
d = double_letter = Space(mult_letter=2, display=DISPLAY_DOUBLE_LETTER)
T = triple_word = Space(mult_word=3, display=DISPLAY_TRIPLE_WORD)
D = double_word = Space(mult_word=2, display=DISPLAY_DOUBLE_WORD)


new_board_string = """
. . . # . . 3 . 3 . . # . . .
. . 2 . . @ . . . @ . . 2 . .
. 2 . . 2 . . . . . 2 . . 2 .
# . . 3 . . . @ . . . 3 . . #
. . 2 . . . 2 . 2 . . . 2 . .
. @ . . . 3 . . . 3 . . . @ .
3 . . . 2 . . . . . 2 . . . 3
. . . @ . . . . . . . @ . . .
3 . . . 2 . . . . . 2 . . . 3
. @ . . . 3 . . . 3 . . . @ .
. . 2 . . . 2 . 2 . . . 2 . .
# . . 3 . . . @ . . . 3 . . #
. 2 . . 2 . . . . . 2 . . 2 .
. . 2 . . @ . . . @ . . 2 . .
. . . # . . 3 . 3 . . # . . .
"""


def build_tree():
    import tree
    from os import path
    file_name = path.join(path.dirname(path.abspath(__file__)), 'enable1-wwf-v4.0-wordlist.txt')
    return tree.build_tree(file_name)

points = dict([(le, v) for le, v, c in tile_tuples])

#todo: make a pool of Score objects if allocation gets painful

class ScoreFactory(object):

    @staticmethod
    def make():
        return Score()

class Score(object):

    def __init__(self):
        self.running = 0
        self.word_multipliers = []
        self.got_crossword_points = False

    def __repr__(self):
        return str(self.get())

    def clear(self):
        self.running = 0
        self.got_crossword_points = False
        del self.word_multipliers[:]

    def copy(self):
        s = Score()
        s.running = self.running
        s.word_multipliers = list(self.word_multipliers) if self.word_multipliers else []
        s.got_crossword_points = self.got_crossword_points
        return s

    def copy_and_add(self, letter, space_char, crossword_points=0):
        s = self.copy()
        s.add(letter, space_char)
        if crossword_points:
            s.running += crossword_points
            s.got_crossword_points = True
        return s

    def add(self, letter, space_char=DISPLAY_EMPTY):
        letter=letter.lower()
        if space_char == DISPLAY_EMPTY:
            self.running += points[letter]
        elif space_char == DISPLAY_DOUBLE_LETTER:
            self.running += 2*points[letter]
        elif space_char == DISPLAY_TRIPLE_LETTER:
            self.running += 3*points[letter]
        elif space_char == DISPLAY_DOUBLE_WORD:
            self.running += points[letter]
            self.word_multipliers.append(2)
        elif space_char == DISPLAY_TRIPLE_WORD:
            self.running += points[letter]
            self.word_multipliers.append(3)

    def get(self):
        total = self.running
        for m in self.word_multipliers:
            total *= m
        return total
