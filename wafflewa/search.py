from points import point_values

class Search(object):

    def __init__(self, tree):
        self.root = tree

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

    @staticmethod
    def score_raw_word(word):
        sum = 0
        for letter in word:
            sum += point_values[letter]
        return sum

    def tell(self, s, top_k=10):
        s = s.lower()
        words = self.enumerate_letters(s)
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

        return sorted(pairs, cmp)[:top_k]

import time
def main():
    start = time.time()
    build("tree2.txt")
    print "build time = %s secs" % (time.time() - start)
    start = time.time()
    dfs(root, '')
    print "walk/print time = %s secs" % (time.time() - start)
    print "count=%s" % count



if __name__ == '__main__':
    main()
