
def get_plays(r, c, pairs):
    return [(word, points, r, c) for word, points in pairs]

def merge_plays(a, b, r, c, k=10):
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


m = [('a', 30), ('b', 22), ('c', 9), ('d', 9), ('e', 8)]
n = [('A', 42), ('B', 19), ('C', 9), ('D', 7)]
print str(merge_plays(m, n))
m = [('a', 30), ('b', 22), ('c', 9), ('d', 9), ('e', 8)]
n = [('A', 42), ('B', 19), ('C', 9), ('D', 7)]
print str(merge_plays(n, m))

m = []
n = [('A', 42), ('B', 19), ('C', 9), ('D', 7)]
print str(merge_plays(n, m))
