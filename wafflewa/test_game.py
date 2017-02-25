

board_str1 = """
    0 1 2 3 4 5 6 7 8 9 A B C D E
  +-------------------------------+
0 | . . . # . . 3 . 3 . . # . . . |
1 | . . 2 . . @ . . . @ . . 2 . . |
2 | . 2 . . 2 F . . . . 2 . . 2 . |
3 | # . P U L L . @ . . . 3 . . # |
4 | . . 2 . . A R R O W . . 2 . . |
5 | . @ . T A P E . . 3 . . . @ . |
6 | 3 . . . 2 . . . . . 2 . . . 3 |
7 | . . . @ . . . . . . . @ . . . |
8 | 3 . . . 2 . . . . . 2 . . . 3 |
9 | . @ . . . 3 . . . 3 . . . @ . |
A | . . 2 . . . 2 . 2 . . . 2 . . |
B | # . . 3 . . . @ . . . 3 . . # |
C | . 2 . . 2 . . . . . 2 . . 2 . |
D | . . 2 . . @ . . . @ . . 2 . . |
E | . . . # . . 3 . 3 . . # . . . |
  +-------------------------------+
"""

from game import create_wwf_game
game = create_wwf_game(board_str1)
print str(game.board)
rack = 'vansoer'
print "'%s' - %s" % (rack, game.get_best(rack))
rack = 'burrito'
print "'%s' - %s" % (rack, game.get_best(rack))

