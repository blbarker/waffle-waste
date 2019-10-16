"""
Get the best play...

Edit overlay and letters in this file and run

Note: a standard tile played on the board must use uppercase
Note: a blank tile played on the board as some letter must use lowercase

Note: a blank tile in your rack of letters is encoded with a ' ' space char
"""

copy_me_overlay = """
```````````````
```````````````
```````````````
```````````````
```````````````
```````````````
```````````````
```````````````
```````````````
```````````````
```````````````
```````````````
```````````````
```````````````
```````````````
"""

# edit overlay and letters (uppercase, unless played blank)
overlay = """
````````JETTY``
```````FER`````
``````FIT``````
A````CANED`````
Q``````A```````
UP``TWILLED````
AL`````E``R````
`A`MOONS`VAUS``
SCRAPE````K`I``
HE`YE```ATE`B``
AT``NUB`XI``L``
D````MOVER`HILI
`````````T``N``
`````````H``G``
`````````SOW```
"""

letters = 'neghgdu'  # blanks are ' ' spaces


from wafflewa.game import create_wwf_game
game = create_wwf_game()
game.board.overlay(overlay)
print str(game.board)
print "Letters: '%s'" % letters.upper()

moves = game.get_best(letters, top_k=12)
print str(moves)
