

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

overlay1 = """
```````````````
```````````````
```````````````
```````````````
```````````````
```````````````
``````BURRITO``
```````````````
```````````````
```````````````
```````````````
```````````````
```````````````
```````````````
```````````````
"""

from game import create_wwf_game
game = create_wwf_game(board_str1)
print str(game.board)
rack = 'vansoer'
print "'%s' - %s" % (rack, game.get_best(rack))
rack = 'burrito'
print "'%s' - %s" % (rack, game.get_best(rack))

game.board.overlay(overlay1)

print str(game.board)

game.board.play("WISH", 5, 10, True)

print str(game.board)

moves = game.get_best('animalx')
print str(moves)

game.board.play(moves[1])
print str(game.board)


game.play("BLUE", 10, 6, 'h')

moves = game.get_best('o mpute')
print(moves)
game.play(moves[0])

game2 = create_wwf_game()
print str(game2)
#print str(game2.get_best('qwertyo'))
print str(game2.get_best_first_move('qwertyo'))
game2.play('QWERTY', 7, 3, 'h')
best = game2.get_best('etuick ')
print str(best)
game2.play(best[0])
#game2.play('TOWERY', 7, 3, 'h')
