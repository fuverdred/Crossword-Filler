class Position():
    '''
    A position is a space for a word in the grid
    '''
    def __init__(self, puzzle, i, j, length, direction):
        self.puzzle = puzzle #  Puzzle() which contains this position
        self.i = i
        self.j = j
        self.length = length
        self.direction = direction
        self.slice = self.get_slice() #  Store positions as a numpy slice for easy access
        self.crossers = dict() #dict of positions which intersect with this one
        self.filled = False
        self.number = None #  Clue number for printing the grid
        self.coords = self.get_cell_coords()
        self.cells = [] #  For storing the cells in the GUI
        self.pattern = re.compile('.'*self.length)
        self.freedom = len(self.puzzle.full_dic[self.length])

    def get_slice(self):
        '''The slice of numpy array which forms this position'''
        if self.direction == 'a':
            return np.s_[self.i, self.j:self.j+self.length]
        else:
            return np.s_[self.i:self.i+self.length, self.j]

    def get_cell_coords(self):
        '''A list of grid coords which make up this position'''
        if self.direction == 'a':
            return [(self.i, j) for j in range(self.j, self.j+self.length)]
        else:
            return [(i, self.j) for i in range(self.i, self.i+self.length)]

    def __repr__(self):
        return str((self.i, self.j, self.length, self.direction))
