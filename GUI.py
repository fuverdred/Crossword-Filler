from collections import defaultdict
import tkinter as tk
from tkinter import ttk
from copy import deepcopy


from Puzzle_class import Puzzle

class Grid_cell(tk.Entry):
    '''
    Each white space on the crossword grid will be one of these
    '''
    def __init__(self, master, puzzle, i, j):
        self.text = tk.StringVar() #  Any characters entered stored here
        super().__init__(master,
                         textvariable=self.text,
                         width=2,
                         relief='ridge',
                         justify='center',
                         font = 'Helvetica 22')
        
        self.puzzle = puzzle #  Link to the back end
        self.i = i
        self.j = j
        self.positions = [] #  Maximum of two if the cell is at a crossing

        # All of the bindings for entry and navigation:
        self.text.trace('w', lambda *args: self.clean_text())
        self.bind('<Button-1>',
                  lambda x: self.master.master.toggle_position(self))
        self.bind('<BackSpace>', self.backspace)
        self.bind('<Right>', self.right)
        self.bind('<Left>', self.left)
        self.bind('<Up>', self.up)
        self.bind('<Down>', self.down)

    def set_number(self, number):
        self.number = number
        self.label = tk.Label(self, text=str(number), bg='white',
                              font='Helvetica 4')
        self.label.place(relx=0, x=0, y=-1, anchor=tk.NW)

    def clean_text(self):
        '''
        Only allow one alpha character to be entered, convert all input
        to upper case. Update backend and shift cursor to next cell
        '''
        if len(self.text.get()) > 0:
            if not self.text.get()[-1].isalpha():
                self.text.set('')
            else:
                self.text.set(self.text.get()[-1].upper())

        self.puzzle.grid[self.i][self.j] = self.text.get() # update backend
        # Push focus to next cell in position
        position = self.master.master.current_position
        index = position.cells.index(self)
        if self.text.get().isalpha() and index < position.length - 1:
            self.master.master.highlight_position(position.cells[index + 1],
                                                  position)

    def backspace(self, event):
        position = self.master.master.current_position
        index = position.cells.index(self)
        if index > 0 and self.text.get() == '': #  backspace text first
            self.master.master.highlight_position(position.cells[index - 1],
                                                  position)
        else: #  If the cursor has ended up on the left of text delete anyway
            self.text.set('')

    def try_cell(self, i, j):
        '''
        Check if a cell exists in the grid at (i, j), if it does highlight it
        '''
        cell = self.master.grid_slaves(i, j)
        if cell == []:
            return  #  Does not exist
        #Keep the current position highlighted if possible
        if self.master.master.current_position in cell[0].positions:
            self.master.master.highlight_position(cell[0],
                                            self.master.master.current_position)
        else:
            self.master.master.highlight_position(cell[0], cell[0].positions[0])

    def right(self, event): #  Arrow key navigation
        self.try_cell(self.i, self.j + 1) #  Can go off grid in +ve direction

    def left(self, event): #  Arrow key navigation
        if self.j != 0: #  Prevent leaving the grid
            self.try_cell(self.i, self.j - 1)

    def up(self, event): #  Arrow key navigation
        if self.i != 0: #  Prevent leaving the grid
            self.try_cell(self.i - 1, self.j)

    def down(self, event): #  Arrow key navigation
        self.try_cell(self.i + 1, self.j) #  Can go off grid in +ve direction


class Application(tk.Frame):
    def __init__(self, master, puzzle):
        super().__init__(master)

        self.puzzle = puzzle #  Back end

        self.grid = tk.Frame(self, bg='black')
        self.grid.pack(side='right')

        self.word_list = tk.Listbox(self, width=21, font = 'Helvetica')
        self.word_list.pack(side='left', fill='y')
        self.word_list.bind('<Double-Button>', lambda _: self.enter_word(
            self.current_position,
            self.current_position.possibles[self.word_list.curselection()[0]]))

        self.cells = [] #  Store the Entry widgets
        self.make_grid()

        self.current_position = None # Start with no position highlighted
        self.current_cell = None #  Start with no cell highlighted

    def make_grid(self):
        for pos in self.puzzle.positions:
            for index, (i, j) in enumerate(pos.coords):
                cell = self.grid.grid_slaves(i, j)
                if self.grid.grid_slaves(i, j) == []:
                    cell = Grid_cell(self.grid, self.puzzle, i, j)
                    self.cells.append(cell)
                    cell.grid(row=i, column=j, padx=1, pady=1)
                else:
                    cell = cell[0] #  cell is already in the grid
                if index == 0:
                    cell.set_number(pos.number)
                pos.cells.append(cell) # Link position to cell
                cell.positions.append(pos) #  link cell to positions it is in

    def colour(self, position):
        '''Sets the colour of a position depending on its freedom'''
        def rgb(r, g, b): #  Convert to colour tkinter can handle
            return '#%s%s%s' % tuple([hex(c)[2:].rjust(2, '0')
                                      for c in (r,g,b)])
        if position.filled or position.pattern.pattern == '.'*position.length:
            return 'white'
        elif position.freedom == 0:
            return 'gray' #  Stupid american spelling
        freedom = position.freedom if position.freedom < 255 else 255
        g = freedom * 2 if freedom < 128 else 255
        r = 255 if freedom < 128 else 255 - (freedom - 128) * 2
        return rgb(r, g, 0)

    def toggle_position(self, cell):
        '''
        If a new position has been clicked highlight that position.
        If the position is already highlighted and a cell at a crossing has
        been clicked toggle to the crossing position
        '''
        if self.current_cell is cell and len(cell.positions) > 1:
            index = cell.positions.index(self.current_position)
            self.highlight_position(cell, cell.positions[index - 1])
        else:
            self.highlight_position(cell, cell.positions[0])

    def highlight_position(self, cell, position):
        '''
        Colour in the current position, with the current cell a slightly
        different shade.
        '''
        if (self.current_position is not None and
            self.current_position is not position):
            self.unhighlight_position(self.current_position)
        self.current_position = position #  Update current position
        self.update_word_list(position)
        self.current_cell = cell
        cell.focus_set() #  Put the cursor into current cell
        for c in position.cells:
            if c is cell:
                c.config(bg='lightblue4') #  different shade to rest of pos
            else:
                c.config(bg='lightblue1')

    def unhighlight_position(self, position):
        '''
        1. Check if the position has changed, if it has recalculate freedom
        2. recalculate freedom of crossers if they have changed
        '''
        if position.pattern != self.puzzle.get_pattern(position):
            self.puzzle.update_position(position)
            for pos in position.crossers:
                if pos.pattern != self.puzzle.get_pattern(pos):
                    self.puzzle.update_position(pos)

        colour = self.colour(position)
        for cell in position.cells:
            if any([pos.filled for pos in cell.positions]):
                cell.config(bg='white') #  Filled crossers take precedence
            else:
                cell.config(bg=colour)

    def update_word_list(self, position):
        self.word_list.delete(0, 'end')
        for word in position.possibles:
            self.word_list.insert('end', word)

    def enter_word(self, position, word):
        self.highlight_position(position.cells[0], position)
        assert len(word) == position.length, "Word does not fit"
        for i, char in enumerate(word):
            position.cells[i].text.set(char)
        
                    

#### LOAD GRIDS AND WORDS #################################################
dic = defaultdict(list)
theme_dic = defaultdict(list)

with open('clean_dictionary.txt', 'r') as f:
    for word in f.readlines():
        dic[len(word[:-1])].append(word[:-1]) #  remove trailing \n

with open('themes/tube_stations.txt', 'r') as f:
    for word in f.readlines():
        theme_dic[len(word[:-1])].append(word[:-1]) #  remove trailing \n

with open('raw_grids.txt', 'r') as f:
    raw_grids = [grid[:-1] for grid in f.readlines()]
############################################################################

puzzles = [Puzzle(grid, dic) for grid in raw_grids]

for i, puzzle in enumerate(puzzles, 1):
    print(i)
    theme = deepcopy(theme_dic)
    puzzle.heuristic_theme_filler(theme)

puzzles.sort(key = lambda x: len(x.positions)-len(x.unfilled), reverse=True)
for p in puzzles[:15]:
    print('{:d}\t{:d}\t{:.3f}'.format(len(p.positions),
                                len(p.positions)-len(p.unfilled),
                                (len(p.positions)-len(p.unfilled))/len(p.positions)))
    

def setup_puzzle(puzzle):
    root = tk.Tk()
    app = Application(root, puzzle)
    app.pack()

    for pos in (set(puzzle.positions) - set(puzzle.unfilled)):
        word = ''.join(puzzle.grid[pos.slice])
        app.enter_word(pos, word)

    for pos in puzzle.unfilled:
        pos.possibles = puzzle.get_possible_words(pos)
    for pos in puzzle.unfilled:
        puzzle.update_position(pos)
    return root, app
