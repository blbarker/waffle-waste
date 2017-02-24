from wafflewa.game import create_wwf_test_board, create_wwf_search

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


b1 = """
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

import time
b = create_wwf_test_board(b1)
print str(b)
start = time.time()
search = create_wwf_search()
end = time.time()
print "create search time = %s" % (end-start)

print "te a word? = %s" % search.is_word("te")
print "go!"
start = time.time()
series = b.get_row_series(search, 4)
end = time.time()
print "time = %s" % (end-start)

print "4 series=%s" % series

series = b.get_row_series(search, 6)
print "6 series=%s" % series
series.ptr = 1
print str(search.tell3('vansoer', series))

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


answer = []
for r in xrange(15):
    s = b.get_row_series(search, r)
    for c in xrange(15):
        s.reset_index(c)
        pairs = search.tell3('vansoer', s)
        plays = get_plays(r, c, pairs)
        answer = merge_plays(answer, plays, 10)

print "answer=%s" % answer


