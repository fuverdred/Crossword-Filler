import numpy as np

class Grid():
    def __init__(self, raw):
        self.raw = raw
        self.size = int(np.sqrt(len(raw)))
        self.divider = '#'
        assert np.isclose(np.sqrt(len(raw)), self.size) #  Check grid is square
        self.grid = np.array([i for i in raw]).reshape((self.size, -1))
        self.positions = self.get_positions()
        self.get_crossers()

    def get_positions(self):
        '''
        Split each row and column of the grid into a string and split
        the string by the dividers. Any spaces for words are greater
        than length 1 and are indexed.
        '''
        def parse_string(string):
            index = 0
            positions = []
            for block in string.split(self.divider):
                if len(block) > 1:
                    positions.append((index, len(block)))
                index += len(block) + 1 #  Always + 1 because the divider is 1
            return positions
        positions = []
        for i,row in enumerate(self.grid):
            across = parse_string(''.join(row))
            if across:
                for index, length in across:
                    positions.append(Position(i, index, length, 'a'))
            down = parse_string(''.join(self.grid[:,i]))
            if down:
                for index, length in down:
                    positions.append(Position(index, i, length, 'd'))
        return positions

    def get_crossers(self):
        '''
        Add any locations of crossings to the dictionary of crossers
        in each Position class in self.positions.
        '''
        for across in [p for p in self.positions if p.direction == 'a']:
            for down in [p for p in self.positions if p.direction == 'd']:
                if across.j <= down.j < across.j + across.length and\
                   down.i <= across.i < down.i + down.length:
                    across.crossers.append(down)
                    down.crossers.append(across)

    def enter_word(self, word, position):
        assert len(word) == position.length, 'Word does not fit'
        word = np.array(list(word))
        self.grid[position.slice] = word
        position.filled = True

    def remove_word(self, regex, position):
        assert len(regex.pattern) == position.length, 'Removal too long'
        blanks = np.array([c if c.isalpha() else ' ' for c in regex.pattern])
        self.grid[position.slice] = blanks
        position.filled = False
        
class Position():
    def __init__(self, i, j, length, direction):
        self.i = i
        self.j = j
        self.length = length
        self.direction = direction
        self.get_slice() #  Store positions as a numpy slice for easy access
        self.crossers = []
        self.freedom = 0
        self.filled = False

    def get_slice(self):
        if self.direction == 'a':
            self.slice = np.s_[self.i, self.j:self.j+self.length]
        else:
            self.slice = np.s_[self.i:self.i+self.length, self.j]

    def __repr__(self):
        return str((self.i, self.j, self.length, self.direction))

