from collections import defaultdict
import tkinter as tk
from tkinter import ttk


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

    def set_number(self, number):
        self.number = number
        self.label = tk.Label(self, text=str(number), bg='white',
                              font='Helvetica 4')
        self.label.place(relx=0, x=0, y=-1, anchor=tk.NW)

    def clean_text(self):
        if len(self.text.get()) > 0:
            if not self.text.get()[-1].isalpha():
                self.text.set('')
            else:
                self.text.set(self.text.get()[-1].upper())


class Application(tk.Frame):
    def __init__(self, master, puzzle):
        super().__init__(master)

        self.puzzle = puzzle #  Back end

        self.grid = tk.Frame(self, bg='black')
        self.grid.pack()

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

    def highlight_position(self, cell, position):
        '''
        Colour in the current position, with the current cell a slightly
        different shade.
        '''

    def unhighlight_position(self, position):
        
        
                    

#### LOAD GRIDS AND WORDS #################################################
dic = defaultdict(list)
theme_dic = defaultdict(list)

with open('clean_dictionary.txt', 'r') as f:
    for word in f.readlines():
        dic[len(word[:-1])].append(word[:-1]) #  remove trailing \n

with open('themes/chocolate_bars.txt', 'r') as f:
    for word in f.readlines():
        theme_dic[len(word[:-1])].append(word[:-1]) #  remove trailing \n

with open('raw_grids.txt', 'r') as f:
    raw_grids = [grid[:-1] for grid in f.readlines()]
############################################################################

puzzle = Puzzle(raw_grids[7], dic) #  This is the back end

root = tk.Tk()
app = Application(root, puzzle)
app.pack()
