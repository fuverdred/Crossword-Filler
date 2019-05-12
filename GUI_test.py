import tkinter as tk
from collections import defaultdict
import re
from copy import deepcopy
from random import choice, shuffle

import numpy as np

from Grid_class import Puzzle #  Format which puzzles/positions are stored in
import sparse_filler as sf #  This contains all of the grid filling tools

class Grid_cell(tk.Frame):
    '''Each text tile in the grid is one of these'''
    def __init__(self, master, puzzle, i, j):
        super().__init__(master)
        self.master = master
        self.puzzle = puzzle #  Reference to the back end for updating
        self.i = i
        self.j = j
        self.positions = [] #  Maximum of two values, normally one
        
        self.text = tk.StringVar()
        self.entry_widget = tk.Entry(self, width=2,
                                     textvariable=self.text,
                                     justify='center',
<<<<<<< HEAD
                                     relief='ridge',
                                     font = "Helvetica 22 bold")
        self.entry_widget.bind('<Button-1>',
            lambda x: self.puzzle.GUI.highlight_position(self, self.positions[0]))
        self.entry_widget.bind('<Right>', )
=======
                                     font = "Helvetica 16 bold")
>>>>>>> 20439591239f64f7c74d6e51ca6f10de5633a765
        self.text.trace('w', lambda *args: self.callback())
        self.entry_widget.grid(row=1, column=1,
                               rowspan=4, columnspan=4,
                               ipadx=4, ipady=4)

    def set_number(self, number):
        self.number = number
        self.label = tk.Label(self.entry_widget, text=str(self.number),
                          bg='white', font="Helvetica 6")
        self.label.place(relx=0, x=0, y=-1, anchor=tk.NW)

    def callback(self):  
        if len(self.text.get()) > 0: #  upper case alpha chars only
            if not self.text.get()[-1].isalpha():
                self.text.set('')
            else:
                self.text.set(self.text.get()[-1].upper())

        self.puzzle.grid[self.i][self.j] = self.text.get() #  update back end
        try:
            position = self.master.master.current_position
            next_cell = position.cells[position.cells.index(self) + 1]
            self.master.master.highlight_position(next_cell,
                                                  position)
            next_cell.entry_widget.focus_set()
        except IndexError:
            pass

            

    def enter_letter(self, letter):
        self.entry_widget.insert(0, letter)

    def colour(self, pos):
        '''Sets the colour of the squares depending on their freedom'''
        def rgb(r, g, b): #  convert to type which tkinter can handle
            return "#%s%s%s" % tuple([hex(c)[2:].rjust(2, '0')
                                      for c in (r, g, b)])
        if pos.filled:
            return 'white'
        elif pos.freedom == 0:
            return 'gray'
        freedom = pos.freedom
        if freedom > 255: #  more than 255 possibles leave fully green
            freedom = 255
        g = freedom*2 if freedom < 128 else 255
        r = 255 if freedom < 128 else 255 - (freedom - 128)*2
        return rgb(r, g, 0) #  colour the square should now be

class Grid(tk.Frame):
    def __init__(self, master, puzzle):
        super().__init__(master)
        self.master = master
        self.puzzle = puzzle #  Link to the puzzle back end
        self.pack()
        self.current_position = None
        self.current_cell = None

        self.grid_canvas = tk.Frame(self, width=100, height=100,
                                    bg='black') #  black background 
        self.grid_canvas.pack()
        self.draw_grid()

    def draw_grid(self):
        self.cells = []
        for i, row in enumerate(self.puzzle.grid):
            for j, val in enumerate(row):
                if val != self.puzzle.divider:
                    cell = Grid_cell(self.grid_canvas, puzzle, i, j)
                    self.cells.append(cell)
                    cell.grid(row=i, column=j, padx=1, pady=1)
                    for p in self.puzzle.positions:
                        if (i, j) == (p.i, p.j):
                            cell.set_number(p.number)
                        if (i, j) in p.coords:
                            #  Give cell and positions each others location
                            p.cells.append(cell)
                            cell.positions.append(p)
    def colour(self, pos):
        '''Sets the colour of the squares depending on their freedom'''
        def rgb(r, g, b): #  convert to type which tkinter can handle
            return "#%s%s%s" % tuple([hex(c)[2:].rjust(2, '0')
                                      for c in (r, g, b)])
        if pos.filled:
            return 'white'
        elif pos.freedom == 0:
            return 'gray'
        freedom = pos.freedom
        if freedom > 255: #  more than 255 possibles leave fully green
            freedom = 255
        g = freedom*2 if freedom < 128 else 255
        r = 255 if freedom < 128 else 255 - (freedom - 128)*2
        return rgb(r, g, 0) #  colour the square should now be
    
    def enter_word(self, position, word):
        assert position.length == len(word), "Word does not fit"
        for i, char in enumerate(word):
            position.cells[i].enter_letter(char)
            position.cells[i].config(bg='white')

    def highlight_position(self, cell, position):
        if (self.current_position is not None and
            self.current_position is not position):
            self.unhighlight_position(self.current_position)
        self.current_position = position
        self.current_cell = cell
        for c in position.cells:
            if c is cell:
                c.entry_widget.config(bg='lightblue4')
            else:
                c.entry_widget.config(bg='lightblue1')

    def unhighlight_position(self, position):
        self.puzzle.update_position(position)
        if position.filled:
            colour = 'white'
        else:
            colour = self.colour(position)
        for cell in position.cells:
            if any([pos.filled for pos in cell.positions]):
                cell.entry_widget.config(bg='white')
            else:
                cell.entry_widget.config(bg=colour)

    def right_key(self, event):
        pass


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


Window = tk.Tk()
Window.geometry("800x800") # heightxwidth+x+y

mainPanel = tk.Canvas(Window, width = 200, height = 200) # main screen
mainPanel.pack()

puzzle = Puzzle(raw_grids[17], dic) #  This is the back end
grid = Grid(mainPanel, puzzle)
puzzle.GUI = grid

##puzzle.heuristic_theme_filler(theme_dic)
##
##filled = [p for p in puzzle.positions if p.filled]
##for pos in filled:
##    print(''.join(puzzle.grid[pos.slice]))
##    for cell in pos.cells:
##        cell.entry_widget.insert(0, puzzle.grid[cell.i][cell.j])
