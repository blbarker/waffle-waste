import random


class Tile(object):
    def __init__(self, letter, value):
        self.letter = letter.lower()
        self.value = value

    def __repr__(self):
        return "%s (%s)" % (self.letter.upper(), self.value)

    def display(self):
        return self.letter.upper()


class PlayedBlankTile(Tile):
    def __init__(self, played_as_letter):
        super(PlayedBlankTile, self).__init__(played_as_letter, 0)

    def display(self):
        return self.letter.lower()  # played blank shows as lowercase (convention)


class TileBag(object):

    @staticmethod
    def create(tile_tuples=None, seed=None):
        tiles = []
        for letter, value, count in tile_tuples:
            tiles.extend([Tile(letter, value) for c in xrange(count)])
        return TileBag(tiles, seed=seed)

    def __init__(self, tiles, seed=None):
        self.tiles = list(tiles)
        if seed:
            random.seed = seed
        random.shuffle(self.tiles)

    @property
    def count(self):
        return len(self.tiles)

    def random_draw(self, n):
        """randomly draw from the tiles (only use in 'play' mode, usually you just keeping sync with 'real' game)"""
        num_to_draw = min(len(self.tiles), n)
        return [self.tiles.pop() for x in xrange(num_to_draw)]

    def add(self, tiles):
        # todo: error handling (probably global with the board, racks, and this bag)
        self.tiles.extend(tiles)

    def remove(self, letter):
        victim_index = None
        for i, tile in enumerate(self.tiles):
            if tile.letter == letter:
                victim_index = i
                break
        if victim_index is None:
            raise RuntimeError("Could not find letter %s in the bag" % letter.upper())
        return self.tiles.pop(victim_index)

    def _get_show_str(self):
        num_columns = 5

        from collections import defaultdict
        d = defaultdict(int)
        for tile in self.tiles:
            d[tile.letter] += 1

        s = sorted(list(d.iteritems()))
        # add dummies until multiple of num_columns
        while len(s) % num_columns != 0:
            s.append((None, None))
        num_rows = len(s) / num_columns

        def get_row(row_index):
            row = []
            for c in xrange(num_columns):
                index = c*num_rows+row_index
                letter, count = s[index]
                if letter is not None:
                    row.append("%s - %s" % (letter.upper(), count))
            return '\t'.join(row)

        rows = [get_row(r) for r in xrange(num_rows)]

        return '\n'.join(rows)

    def show(self):
        """print the contents of the tile bag"""
        print self._get_show_str()
        print
        print "count = %s" % self.count


class Rack(object):

    def __init__(self, capacity, tiles=None):
        self.capacity = capacity  # the max (or standard) number of tiles
        self.tiles = tiles or []

    def __repr__(self):
        return self._get_show_str()

    def copy(self, fresh_tiles):
        return Rack(self.capacity, fresh_tiles)

    def get_letters(self):
        return ''.join([tile.letter for tile in self.tiles])

    def add(self, tile):
        if len(self.tiles) >= self.capacity:
            raise RuntimeError("Cannot add more tiles, already have %s:  %s" % (self.capacity,self._get_show_str()))
        self.tiles.append(tile)

    def remove(self, letter, allow_missing=False):
        if not self.tiles and not allow_missing:
            raise RuntimeError("Cannot remove any tiles, there are none in this rack!")
        victim_index = None
        for i, tile in enumerate(self.tiles):
            if tile.letter == letter:
                victim_index = i
                break
        if victim_index is None:
            if not allow_missing:
                raise RuntimeError("Could not find letter %s in the rack: %s" % (letter.upper(), self._get_show_str()))
            return None
        return self.tiles.pop(victim_index)

    def _get_show_str(self):
        letters, values = zip(*[(tile.letter.upper(), tile.value) for tile in self.tiles])
        #letters, values = zip() return "\t".join((tile.letter.upper(), tile.value) for tile in self.tiles])
        return '%s\n%s' % ("  ".join([' %s ' % letter for letter in letters]),
                           "  ".join(['(%s)' % (value if value < 10 else 'X') for value in values]))


class Play(object):

    def __init__(self, board, vertical):
        self.board = board
        self.tiles
        self.vertical = vertical  # bool
        self.staged = []  # list of (tile, r, c) to be played
        self.words = []  # list of (word, score) that will result from the play

    @property
    def score(self):
        return sum(score for word, score in self.words)

    def stage(self, tile, space):
        self.staged.append((tile, space))

    def dump(self):
        dumped = [tile for tile, space, in self.staged]
        self.staged = []
        return dumped

    def __repr__(self):
        return "%s for %s" % (self.score, ', '.join(['%s-%s' % (word, score) for word, score in self.words]))

