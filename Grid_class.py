from collections import defaultdict
from copy import deepcopy
import re
from random import shuffle

import numpy as np

class Puzzle():
    def __init__(self, raw, full_dic):
        self.raw = raw
        self.full_dic = full_dic #  For arc consistency and grid completion
        self.size = int(np.sqrt(len(raw)))
        self.divider = '#' #  Represents dark squares on the grid
        assert np.isclose(np.sqrt(len(raw)), self.size) #  Check grid is square
        self.grid = np.array([i for i in raw]).reshape((self.size, -1))
        self.positions = self.get_positions()
        self.unfilled = self.positions[:]
        self.number_positions()
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
                    positions.append(Position(self, i, index, length, 'a'))
            down = parse_string(''.join(self.grid[:, i])) # column i
            if down:
                for index, length in down:
                    positions.append(Position(self, index, i, length, 'd'))
        return sorted(positions, key = lambda pos: (pos.i, pos.j))

    def number_positions(self):
        '''
        Store the clue numbers for each position, following standard
        crossword numbering rules. This method works because they are already
        ordered.
        '''
        number = 1
        done = []
        for pos in self.positions:
            if (pos.i, pos.j) in done:
                pos.number = number - 1
            else:
                done.append((pos.i, pos.j))
                pos.number = number
                number += 1

    def get_crossers(self):
        '''
        Add any locations of crossings to the list of crossers
        in each Position in self.positions.
        '''
        for across in [p for p in self.positions if p.direction == 'a']:
            for down in [p for p in self.positions if p.direction == 'd']:
                if across.j <= down.j < across.j + across.length and\
                   down.i <= across.i < down.i + down.length:
                    across.crossers.append(down)
                    down.crossers.append(across)

    def enter_word(self, position, word):
        assert len(word) == position.length, 'Word does not fit'
        word = np.array(list(word))
        self.grid[position.slice] = word
        position.pattern = self.get_pattern(position) #  update pattern
        position.filled = True
        if position in self.unfilled: #  In case we are overwriting a word
            self.unfilled.remove(position)

    def remove_word(self, position, regex):
        assert len(regex.pattern) == position.length, 'Removal wrong size'
        blanks = np.array([c if c.isalpha() else ' ' for c in regex.pattern])
        self.grid[position.slice] = blanks
        position.pattern = self.get_pattern(position) #  update pattern
        position.filled = False
        if position not in self.unfilled: #  If accidentally removed twice
            self.unfilled.append(position) #  Don't want multiple entries

    def get_pattern(self, position):
        '''Return a compiled regex for the position'''
        return re.compile(''.join([c if c.isalpha() else '.'
                                   for c in self.grid[position.slice]]))

    def get_possible_words(self, position, pattern=None, dic=None):
        '''
        Return a list of possible words which fit position. If checking
        the crossers of a temporary word, the positions pattern will not
        be up to date, hence a pattern is passed in.
        '''
        if pattern is None:
            pattern = position.pattern
        if dic is None:
            dic = self.full_dic
        return [word for word in dic[position.length] if
                re.match(pattern, word)]

    def get_propagation_score(self, position, word):
        '''
        If any given word is entered into position, how many possible
        options for the crossing words does it leave, summed over all of
        the crossers
        '''
        if all([pos.filled for pos in position.crossers]):
            return 1 #  Does not affect the future grid options
        old_pattern = position.pattern #  For removing word afterwards
        self.enter_word(position, word)
        total = 0
        for pos in position.crossers:
            score = len(self.get_possible_words(pos,
                                                self.get_pattern(pos),
                                                self.full_dic))
            if score == 0:
                total = 0 #  This word means the grid cannot be completed
                break
            total += score
        self.remove_word(position, old_pattern)
        return total

    def rank_possible_words(self, position):
        '''
        Rank all of the possible words which fit by their propagation score.
        This method has a LOT of scope for optimisation, current version
        is about as poorly optimised as it gets
        '''
        position.scores = [self.get_propagation_score(position, word)
                           for word in position.possibles]
        temp_zip = sorted(zip(position.scores, position.possibles),
                          key=lambda x: x[0], reverse=True)
        temp_zip = [(score, possible) for score, possible in temp_zip
                    if score] #  Remove any words with a score of 0
        if not temp_zip:
            position.scores = []
            position.possibles = []
        else:
            position.scores, position.possibles = zip(*temp_zip)

    def update_position(self, position):
        '''
        Recalculate the possible words which match a position and update
        the pattern, list of words and freedom of the position. Rank the
        possible words by highest propagation score, while keeping the
        score for reference.
        '''
        position.pattern = self.get_pattern(position)
        if all([c.isalpha() for c in position.pattern.pattern]):
            position.filled = True
            return
        position.possibles = self.get_possible_words(position)
##        position.scores = self.rank_possible_words(position)
##        temp_zip = sorted(zip(position.scores, position.possibles),
##                          key=lambda x: x[0], reverse=True)
##        position.scores, position.possibles = zip(*temp_zip)
        position.freedom = len(position.possibles)

    def grid_print(self):
        for row in self.grid:
            print(''.join(row))

    def fit_theme(self, theme_dic, check_arc_consistency=False):
        def recursive(theme_positions, theme_dic, remaining_pos, depth=0):
            nonlocal best_count
            nonlocal best_grid
            nonlocal check_arc_consistency

            #Check for end of recursion
            if not theme_positions:
                return
            if not any([theme_dic[i] and remaining_pos[i]
                        for i in theme_dic.keys()]):
                return
            
            depth += 1
            print(' '*depth, depth) #  track recursion

            if depth > best_count:
                best_count = depth
                best_grid = deepcopy(self.grid)

            current_pos = theme_positions[0] #  next position to try
            current_pattern = current_pos.pattern #  need for removing word
            possibles = self.get_possible_words(current_pos,
                                                pattern = self.get_pattern(current_pos),
                                                dic=theme_dic)
            if check_arc_consistency:
                possibles = [word for word in possibles if
                             self.get_propagation_score(current_pos, word)]

            if not possibles: # depth-1 because a word has not been entered
                recursive(theme_positions[1:], theme_dic,
                          remaining_pos, depth-1)
            else:
                for word in possibles:
                    self.enter_word(current_pos, word)
                    theme_dic[current_pos.length].remove(word)
                    remaining_pos[current_pos.length] -= 1
                    for pos in current_pos.crossers:
                        if pos in theme_positions: #  Move the crossers to the front
                            theme_positions.insert(1, theme_positions.pop(
                                                    theme_positions.index(pos)))
                    recursive(theme_positions[1:], theme_dic, remaining_pos, depth)
                    self.remove_word(current_pos, current_pattern)
                    theme_dic[current_pos.length].append(word)
                    remaining_pos[current_pos.length] += 1
            
        # Only deal with relevant words and positions   
        theme_positions = [pos for pos in self.positions
                           if pos.length in theme_dic.keys()]
        remove = []
        for word_length in theme_dic.keys():
            if word_length not in {p.length for p in theme_positions}:
                remove.append(word_length)
        for index in remove:
            theme_dic.pop(index)

        remaining_pos = defaultdict(int)
        for pos in theme_positions:
            remaining_pos[pos.length] += 1 #  Tracking open positions left
        
            
        shuffle(theme_positions)

        best_grid = None
        best_count = 0

        recursive(theme_positions, theme_dic, remaining_pos)
        self.grid = best_grid

    def heuristic_theme_filler(self, theme_dic):
        '''
        Fit theme words by ranking them in order of how much freedom they give
        the grid, followed by any theme words which intersect.
        '''
        def get_best_word(position):
            possibles = self.get_possible_words(position,
                                            pattern=self.get_pattern(position),
                                            dic=theme_dic)
            if not possibles:
                return
            position.possibles = possibles
            self.rank_possible_words(position)
            if not position.possibles:
                return
            return position.possibles[0]
            
            
        def weak_recursive(position, depth=0):
            '''Weak because there is minimal backtracking'''
            depth += 1
            #print(' '*depth, depth)

            for pos in position.crossers:
                # Best word leaves the most freedom in the grid
                best_word = get_best_word(pos)
                if best_word is None:
                    continue
                self.enter_word(pos, best_word)
                theme_dic[pos.length].remove(best_word)
                weak_recursive(pos, depth)

        # Only deal with relevant words and positions   
        theme_positions = [pos for pos in self.positions
                           if pos.length in theme_dic.keys()]
        theme_positions.sort(key=lambda x: x.length, reverse=True) # longest 1st
        
        remove = []
        for word_length in theme_dic.keys():
            if word_length not in {p.length for p in theme_positions}:
                remove.append(word_length)
        for index in remove:
            theme_dic.pop(index)#  remove words for which no pos exists

        for pos in theme_positions:
            if pos.filled:
                continue
            best_word = get_best_word(pos)
            if best_word is None:
                continue
            self.enter_word(pos, best_word)
            theme_dic[pos.length].remove(best_word)
            weak_recursive(pos)
        

    def latex_print(self):
        '''In LaTeX mark up for printing'''
        print("\\begin{Puzzle}{15}{15}")
        number = 1 #  Position number eg. 1 across
        for i in range(self.size):
            line = ''
            for j in range(self.size):
                line += '|'
                if self.grid[i][j] == self.divider:
                    line += '*'
                else:
                    if (i,j) in [(p.i, p.j) for p in self.positions]:
                        line += '['+str(number)+']'
                        number += 1
                    if self.grid[i][j] == ' ':
                        line += '{}'
                    else:
                        line += self.grid[i][j]
            print(line + '|.')
        print("\\end{Puzzle}")
        
class Position():
    '''
    A position is a space for a word in the grid, eg. 1 across
    '''
    def __init__(self, puzzle, i, j, length, direction):
        self.puzzle = puzzle #  Puzzle() which contains this position
        self.i = i
        self.j = j
        self.length = length
        self.direction = direction
        self.get_slice() #  Store positions as a numpy slice for easy access
        self.crossers = [] #  List of positions which intersect with this one
        self.filled = False
        self.number = None #  Clue number for printing the grid
        self.get_cell_coords()
        self.cells = [] #  For storing the cells in the GUI
        self.pattern = re.compile('.'*self.length)
        self.freedom = len(self.puzzle.full_dic[self.length])

    def get_slice(self):
        '''The slice of numpy array which forms this position'''
        if self.direction == 'a':
            self.slice = np.s_[self.i, self.j:self.j+self.length]
        else:
            self.slice = np.s_[self.i:self.i+self.length, self.j]

    def get_cell_coords(self):
        '''A list of grid coords which make up this position'''
        coord_grid = np.array([[(i,j) for j in range(self.puzzle.size)]
                               for i in range(self.puzzle.size)])
        self.coords = [(i,j) for i,j in coord_grid[self.slice]]

    def __repr__(self):
        return str((self.i, self.j, self.length, self.direction))


def grid_print(puzzle):
    for row in puzzle.grid:
        print(''.join(row))

if __name__ == '__main__':
    dic = defaultdict(list)
    theme_dic = defaultdict(list)

    with open('clean_dictionary.txt', 'r') as f:
        for word in f.readlines():
            dic[len(word[:-1])].append(word[:-1]) #  remove trailing \n

    with open('themes/chocolate_bars.txt', 'r') as f:
        for word in list(f.readlines()):
            theme_dic[len(word[:-1])].append(word[:-1]) #  remove trailing \n

    with open('raw_grids.txt', 'r') as f:
        raw_grids = [grid[:-1] for grid in f.readlines()]

    test = Puzzle(raw_grids[2], dic)
    test.heuristic_theme_filler(theme_dic)
