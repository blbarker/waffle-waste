from wafflewa.game import create_wwf_search, create_wwf_board

blank = """
...............
...............
...............
...............
...............
...............
...............
...............
...............
...............
...............
...............
...............
...............
...............
"""


overlay = """
```````````````
```````````````
`````F`````````
``PULL`````````
`````ARROW`````
```TAPE````````
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

b2 = """
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

import time
# b = create_wwf_test_board(b1)
# print str(b)
start = time.time()
search = create_wwf_search()
end = time.time()
print "create search time = %s" % (end-start)

# print "te a word? = %s" % search.is_word("te")
# print "go!"
# start = time.time()
# series = b.get_row_series(search, 4)
# end = time.time()
# print "time = %s" % (end-start)
#
# print "4 series=%s" % series
#
# series = b.get_row_series(search, 6)
# print "6 series=%s" % series
# series.ptr = 1
# print str(search.get_word_candidates('vansoer', series, 0))

def merge_plays(a, b, k=10):
    x = []
    while len(a) and len(b):
        if b[0][1] >  a[0][1]:
            x.append(b.pop(0))
        else:
            x.append(a.pop(0))

        if len(x) >= k:
            return x
    while len(a):
        x.append(a.pop(0))
    while len(b):
        x.append(b.pop(0))
    return x

def get_plays(r, c, pairs):
    return [(word, points, r, c) for word, points in pairs]


# answer = []
# for r in xrange(15):
#     s = b.get_row_series(search, r)
#     for c in xrange(15):
#         #s.reset_index(c)
#         pairs = search.get_word_candidates('vansoer', s, c)
#         plays = get_plays(r, c, pairs)
#         answer = merge_plays(answer, plays, 10)
#
# print "answer=%s" % answer
#

board2 = create_wwf_board(b2)
print str(board2)

answer = []
for r in xrange(15):
    s = board2.get_row_series(r)
    for c in xrange(15):
        #s.reset_index(c)
        pairs = search.get_word_candidates('vansoer', s, c)
        plays = get_plays(r, c, pairs)
        answer = merge_plays(answer, plays, 10)

print "answer2=%s" % answer