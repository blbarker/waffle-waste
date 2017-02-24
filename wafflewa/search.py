from points import point_values

class Candidates(object):

    def __init__(self, threshold=10, k=10):
        self.pairs = []
        self.threshold = threshold
        self.k = k

    def consider(self, word, score, require_crossword=False):
        if not score.got_crossword_points and require_crossword:
            return
        points = score.get()
        if points < self.threshold:
            return
        insert_index = -1
        for i, pair in enumerate(self.pairs):
            if word == pair[0]:
                return  # duplicate word
            if points > pair[1]:
                insert_index = i
                break
        if insert_index >= 0:
            self.pairs.insert(insert_index, (word, points))
            if len(self.pairs) > self.k:
                self.pairs.pop()
        elif len(self.pairs) < self.k:
            self.pairs.append((word, points))

    def report(self):
        def comp(a, b):
            if a[1] < b[1]:
                return 1
            if a[1] > b[1]:
                return -1
            if a[0] < b[0]:
                return -1
            if a[0] > b[0]:
                return 1
            return 0
        x = sorted(self.pairs, comp)
        return x

class Search(object):

    def __init__(self, tree, score_factory):
        self.root = tree
        self.score_factory = score_factory

    # def get_score(self, initial_score, letter, space_char):
    #     value = self.letter_values[letter]
    #     if space_char ==

    def is_word(self, s):
        n = self.root
        for letter in s:
            try:
                n = n.kids[letter]
            except:
                return False
        return n.terminal

    def enumerate_letters(self, s):
        words = set()

        def go(node, word, remaining_letters):
            if node.terminal:
                words.add(word)
            if node.kids and remaining_letters:
                for i, letter in enumerate(remaining_letters):
                    if letter in node.kids:
                        go(node.kids[letter], word + letter, remaining_letters[:i] + remaining_letters[i+1:])
        go(self.root, '', s)
        return words

    def enumerate_letters_with_restrictions(self, s, ser):
        words = set()

        def go(node, word, remaining_letters, series):
            if word == 'burrit':
                print "here"
            if node.terminal and series.word_can_end():
                words.add(word)
            if node.kids and not series.at_end():
                series.advance()
                req = series.required()
                if req:
                    if req in node.kids:
                        go(node.kids[req], word + req, remaining_letters, series)
                elif remaining_letters:
                    for i, letter in enumerate(remaining_letters):
                        if letter in node.kids:
                            go(node.kids[letter], word + letter, remaining_letters[:i] + remaining_letters[i+1:], series.copy())
        go(self.root, '', s, ser)
        return words

    def get_word_candidates(self, s, ser, top_k=10, threshold=5):
        candidates = Candidates(threshold=threshold, k=top_k)

        def go(node, word, score, remaining_letters, series):
            if node.terminal and series.word_can_end():
                candidates.consider(word, score)
            if node.kids and not series.at_end():
                series.advance()
                req = series.required()
                if req:
                    if req in node.kids:
                        score.add(req)
                        go(node.kids[req], word + req, score, remaining_letters, series)
                elif remaining_letters:
                    for i, letter in enumerate(remaining_letters):
                        if letter in node.kids:
                            go(node.kids[letter],
                               word + letter,
                               score.copy_and_add(letter, series.current),
                               remaining_letters[:i] + remaining_letters[i+1:],
                               series.copy())
        init_score = self.score_factory.make()
        go(self.root, '', init_score, s, ser)
        return candidates

    def get_word_candidates3(self, s, ser, top_k=10, threshold=5):
        candidates = Candidates(threshold=threshold, k=top_k)

        def go(node, word, score, remaining_letters, series):
            if word == 'rots':
                print "here"
            if node.terminal and series.word_can_end():
                candidates.consider(word, score, require_crossword=True)
            if node.kids and not series.at_end():
                series.advance()
                req = series.required()
                if req:
                    if req in node.kids:
                        score.add(req)
                        go(node.kids[req], word + req, score, remaining_letters, series)
                elif remaining_letters:
                    for i, letter in enumerate(remaining_letters):
                        if letter in node.kids:
                            ok, crossword, crossword_points = series.check_crossword(letter)
                            if ok:
                                go(node.kids[letter],
                                   word + letter,
                                   score.copy_and_add(letter, series.current, crossword_points),
                                   remaining_letters[:i] + remaining_letters[i+1:],
                                   series.copy())
        init_score = self.score_factory.make()
        go(self.root, '', init_score, s, ser)
        return candidates

    def trial_placement(self, board, rack):
        pass

    #def try_space(self, board, rack, r, c, vertical, board, rack):

    @staticmethod
    def score_raw_word(word):
        sum = 0
        for letter in word:
            sum += point_values[letter]
        return sum

    def tell(self, s, series=None, top_k=10):
        s = s.lower()
        words = self.enumerate_letters(s) if series is None else self.enumerate_letters_with_restrictions(s, series)
        pairs = [(word, self.score_raw_word(word)) for word in words]
        def cmp(a, b):
            if a[1] < b[1]:
                return 1
            if a[1] > b[1]:
                return -1
            if a[0] < b[0]:
                return -1
            if a[0] > b[0]:
                return 1

            return 0

        x = sorted(pairs, cmp)[:top_k]
        return x

    def tell2(self, s, series=None, top_k=10, threshold=5):
        s = s.lower()
        candidates = self.get_word_candidates(s, series, top_k=top_k, threshold=threshold)
        return candidates.report()

    def tell3(self, s, series=None, top_k=10, threshold=5):
        s = s.lower()
        candidates = self.get_word_candidates3(s, series, top_k=top_k, threshold=threshold)
        return candidates.report()

from wwf import ScoreFactory


class Series(object):

    NO_CROSSWORD = ('', '')

    def __init__(self, search, s, crosswords=None, index=0):
        self.search = search
        self.s = s
        self.crosswords = crosswords
        self.ptr = index-1

    def __repr__(self):
        return "%s  [%s]" % (self.s, (",".join([str(cw) for cw in self.crosswords]) if self.crosswords else ''))

    def reset_index(self, index):
        self.ptr = index-1

    def copy(self):
        return Series(self.search, self.s, crosswords=self.crosswords, index=self.ptr+1)

    def word_can_end(self):
        """returns whether a word can end in the current position"""
        return self.at_end() or not self.s[self.ptr+1].isalpha()

    def at_end(self):
        """bool indicating no more advancing allowed"""
        return self.ptr >= (len(self.s)-1)

    @property
    def current(self):
        return self.s[self.ptr]

    def required(self):
        """Returns a letter if it is required to be next, else it returns None"""
        c = self.current
        return None if not c.isalpha() else c

    def check_crossword(self, letter):
        index = self.ptr
        space = self.current
        if not self.crosswords or not self.crosswords[index] or ('', '') == self.crosswords[index]:
            return True, '', 0  # There is no crossword, True means it's OK to keep going, no extra points
        pre, post = self.crosswords[index]
        word = pre + letter + post
        if not self.search.is_word(word.lower()):
            return False, None, None  # False means it is NOT OK to keep going
        # score it
        score = ScoreFactory.make()
        score.add(letter, space)
        rest = pre + post
        for let in rest:
            score.add(let)
        return True, word, score.get()

    def advance(self):
        """Advances pointer to next space, returns whether it was successful (bool)"""
        if not self.at_end():
            self.ptr += 1
            return True
        return False


class BoardExplorer(object):
    def __init__(self, board, rack):
        self.board = board
        self.rack = rack
        self.letters = rack.get_letters()

    def go(self, k=3):
        pass

# class SpaceExplorer(object):
#     def __init__(self, board_explorer, r, c):
#         self.board_explorer = board_explorer
#         self.r = r
#         self.c = c
#
#     def horizontal(self):
#         # check forwards and backwards for min length

# import time
# def main():
#     start = time.time()
#     build("tree2.txt")
#     print "build time = %s secs" % (time.time() - start)
#     start = time.time()
#     dfs(root, '')
#     print "walk/print time = %s secs" % (time.time() - start)
#     print "count=%s" % count
#
#
#
# if __name__ == '__main__':
#     main()
