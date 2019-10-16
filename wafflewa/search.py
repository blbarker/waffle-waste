

# note:  Regular tiles show as uppercase
#        Blank tiles that have been played show as lowercase
#        A blank is represent by a space character

class Play(object):
    def __init__(self, word, points, row, col, v_or_h):
        self.word = word
        self.points = points
        self.row = row
        self.col = col
        self.v_or_h = v_or_h

    def __repr__(self):
        return '%s %dpts %s(%X,%X)' % \
               (self.word, self.points, self.v_or_h, self.row, self.col)


class Candidates(object):

    def __init__(self, top_k=10, threshold=10):
        self.plays = []
        self.threshold = threshold
        self.top_k = top_k

    def consider(self, word, score, require_attached=False):
        if not score.attached and require_attached:
            # this makes sure that the word actually connects to another on the board
            # todo: fix broken corner case of an all-blank crossword
            return
        points = score.get_points()
        if points < self.threshold:
            return
        insert_index = -1
        for i, pair in enumerate(self.plays):
            if word == pair[0]:
                return  # duplicate word
            if points > pair[1]:
                insert_index = i
                break
        if insert_index >= 0:
            self.plays.insert(insert_index, (word, points))
            if len(self.plays) > self.top_k:
                self.plays.pop()
        elif len(self.plays) < self.top_k:
            self.plays.append((word, points))

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
        x = sorted(self.plays, comp)
        return x


class Search(object):

    def __init__(self, tree, score_factory):
        self.root = tree
        self.score_factory = score_factory

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
    def merge_plays(a, b, k=10):
        """Merges two lists of plays (destroys them), assumes points are in the second tuple position"""
        x = []
        while len(a) and len(b):
            if b[0].points >  a[0].points:
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

    def get_candidates(self, letters_string, board, top_k=10, threshold=5):
        def get_h(word, points, r, c):
            return Play(word, points, r, c, 'h')

        def get_v(word, points, r, c):
            return Play(word, points, c, r, 'v')

        h = self._get_candidates_for_board(letters_string, board, get_h, top_k, threshold)
        v = self._get_candidates_for_board(letters_string, board.transposed(), get_v, top_k, threshold)
        answer = self.merge_plays(h, v, k=top_k)
        return answer

    def _get_candidates_for_board(self, letters_string, board, get_play, top_k=10, threshold=5):
        answer = []
        for r in xrange(board.num_rows):
            series = board.get_row_series(r)
            for c in xrange(len(series.line)):
                pairs = self.get_candidates_for_space(letters_string, series, c, top_k, threshold)
                plays = [get_play(word, points, r, c) for word, points in pairs]
                answer = self.merge_plays(answer, plays, 10)
        return answer

    def get_candidates_for_first_move(self, start_index, letters_string, board, top_k=10, threshold=5):
        def get_h(word, points, r, c):
            return word, points, r, c, 'h'
        get_play = get_h
        answer = []
        series = board.get_row_series(start_index)
        for c in xrange(len(series.line)):
            pairs = self.get_candidates_for_space(letters_string, series, c, top_k, threshold, require_attached=False)
            plays = [get_play(word, points, start_index, c) for word, points in pairs if
                     (c == start_index or (c < start_index and (c + len(word)) > start_index))]
            answer = self.merge_plays(answer, plays, 10)
        return answer

    def get_candidates_for_space(self, letters_string, board_series, series_index, top_k=10, threshold=5, require_attached=True):
        candidates = Candidates(top_k=top_k, threshold=threshold)
        series = board_series
        num_letters = len(letters_string)

        def go(node, word, score, remaining_letters, index):
            if node.terminal and len(remaining_letters) < num_letters and series.word_can_start_and_end(word, index):
                candidates.consider(word, score, require_attached=require_attached)
            space = series.get_space(index)
            if node.kids and space:
                if space.isalpha():
                    required_letter = space.upper()
                    if required_letter in node.kids:
                        if space.isupper():  # check that it is not a blank, represented by lowercase
                            score.add(space, attached=True)
                        go(node.kids[required_letter],
                           word + required_letter,
                           score,
                           remaining_letters,
                           index + 1)
                elif remaining_letters:
                    for i, letter in enumerate(remaining_letters):
                        is_blank = letter == ' '
                        if is_blank:
                            choices = node.kids.keys()
                        elif letter in node.kids:
                            choices = [letter]
                        else:
                            choices = []
                        for choice in choices:
                            cross = series.get_cross(index)
                            crossword_points = self.check_crossword(choice, space, cross)
                            if crossword_points is not None:
                                go(node.kids[choice],
                                   word + (choice.lower() if is_blank else choice),
                                   score.copy_and_add(letter, space, crossword_points),
                                   remaining_letters[:i] + remaining_letters[i+1:],
                                   index + 1)
        init_score = self.score_factory.make()
        go(self.root, '', init_score, letters_string.upper(), series_index)
        return candidates.report()

    def check_crossword(self, letter, space, cross):
        """
        Checks for a crossword and returns the score of that crossword

        If there is no cross to worry about, a score of 0 is returned
        If there is a cross but the formed crossword is an invalid word, None is returned
        """
        if cross == ('', ''):
            return 0

        pre, post = cross
        crossword = pre + letter + post
        if self.is_word(crossword):
            score = self.score_factory.make()
            score.add(letter, space)
            rest = pre + post
            for let in rest:
                score.add(let)
            return score.get_points()
        return None
