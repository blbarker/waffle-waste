
#from wafflewa.search import Candidates


from wafflewa import create_wwf_game
g = create_wwf_game("burrito")
#print str(g.tell('itoburr'))
# print str(g.search('itoburr', Series('???????', -1)))
# print str(g.search('itoburr', Series('??r????', -1)))
# x = g.search('itoburr', Series('b???', -1))
# four_letter_b = [('bubo', 7),
#                  ('bout', 6),
#                  ('brut', 6),
#                  ('bub', 6),
#                  ('burr', 6),
#                  ('bib', 5),
#                  ('biro', 5),
#                  ('birr', 5),
#                  ('bob', 5),
#                  ('bort', 5)]
# assert  x == four_letter_b
#
#
# print str(g.search('itxburr', Series('??????o', -1)))
#

#for w in ['ta', 'te', 'ti', 'to', 'tu']:
#    print "%s is a word: %s" % (w, g.tree_search.is_word(w))

# print str(g.tell2('burrito', g.make_series('.......'), threshold=3, top_k=20))
# print str(g.tell2('burrito', g.make_series('..2....'), threshold=3, top_k=20))
# print str(g.tell2('burrito', g.make_series('..2.@..'), threshold=3, top_k=20))
# print str(g.tell2('burrito', g.make_series('...3@..'), threshold=3, top_k=20))
# print str(g.tell2('burrito', g.make_series('...n@..'), threshold=3, top_k=20))
# print str(g.tell2('burrito', g.make_series('..d.n..@..', None, 2), threshold=3, top_k=20))
# print str(g.tell2('burrito', g.make_series('..d2.', None, 2), threshold=3, top_k=20))
# print str(g.tell2('burrito', g.make_series('..n2.', crosswords=[em,('t',''),('o',''),em,em]), threshold=3, top_k=20))
em = ('', '')
print str(g.tell3('burrito', g.make_series('..n2.', crosswords=[em,('t',''),('o',''),em,em]), threshold=3, top_k=20))
