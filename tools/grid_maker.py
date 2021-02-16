'''
A simple GUI for making arbitrary square crossword grid layouts for
'''

import random
import tkinter as tk

class Square(tk.Canvas):
    def __init__(self, master, i, j, colour='white'):
        tk.Canvas.__init__(self, master, width=50, height=50)
        self['bg'] = colour
        self.i = i
        self.j = j

        self.bind('<Button-1>', lambda _ : master.toggle(self.i,
                                                         self.j))

class Crossword(tk.Frame):
    def __init__(self, master, size):
        tk.Frame.__init__(self, master)
        
        self.size = size
        self.squares = {}
        self.make_grid()
        
    def make_grid(self):
        for i in range(self.size):
            for j in range(self.size):
                square = Square(self, i, j)
                self.squares[i,j] = square
                square.grid(column=i, row=j)

    def toggle(self, i, j):
        '''
        Simple mirror symmetry in diagonal applied
        '''
        toggle_dic = {'white':'black', 'black':'white'}
        new_colour = toggle_dic[self.squares[i, j]['bg']]

        self.squares[i, j]['bg'] = new_colour
        self.squares[self.size-(i+1), self.size-(j+1)]['bg'] = new_colour

    def reset(self):
        for key in self.squares.keys():
            self.squares[key]['bg'] = 'white'

    def unches_all(self):
        self.reset()
        for i in range(0, self.size, 2):
            for j in range(0, self.size, 2):
                self.squares[i, j]['bg'] = 'black'

    def unches_side(self):
        self.reset()
        for i in range(1, self.size, 2):
            for j in range(0, self.size, 2):
                self.squares[i, j]['bg'] = 'black'

    def unches_top(self):
        self.reset()
        for i in range(0, self.size, 2):
            for j in range(1, self.size, 2):
                self.squares[i, j]['bg'] = 'black'

    def no_unches(self):
        self.reset()
        for i in range(1, self.size, 2):
            for j in range(1, self.size, 2):
                self.squares[i, j]['bg'] = 'black'

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.crossword = Crossword(self, 15)
        self.crossword.pack(side='bottom')

        self.menuBar = tk.Menu(self)
        self.menu_setup()
        self.config(menu=self.menuBar)

    def new_xword(self, size):
        for key in self.crossword.squares.keys():
            self.crossword.squares[key].grid_forget()
            self.crossword.squares[key].destroy
        self.crossword.squares = {}
        self.crossword.size = size
        self.crossword.make_grid()

    def menu_setup(self):
        # file menu
        file_menu = tk.Menu(self.menuBar, tearoff=0)
        file_menu.add_command(label='5x5',
                              command=lambda: self.new_xword(5))
        file_menu.add_command(label='7x7',
                              command=lambda: self.new_xword(7))
        file_menu.add_command(label='9x9',
                              command=lambda: self.new_xword(9))
        file_menu.add_command(label='11x11',
                              command=lambda: self.new_xword(11))
        file_menu.add_command(label='13x13',
                              command=lambda: self.new_xword(13))
        file_menu.add_command(label='15x15',
                              command=lambda: self.new_xword(15))
        self.menuBar.add_cascade(label='File', menu=file_menu)
        # edit menu
        edit_menu = tk.Menu(self.menuBar, tearoff=0)
        edit_menu.add_command(label='No unches',
                              command=self.crossword.no_unches)
        edit_menu.add_command(label='Vertical unches',
                              command=self.crossword.unches_top)
        edit_menu.add_command(label='Side unches',
                              command=self.crossword.unches_side)
        edit_menu.add_command(label='All unches',
                              command=self.crossword.unches_all)
        edit_menu.add_command(label='Clear',
                              command=self.crossword.reset)
        self.menuBar.add_cascade(label='Edit', menu=edit_menu)
        # Symmetry menu
        symmetry = tk.BooleanVar()
        symmetry.set(True)
        sym_menu = tk.Menu(self.menuBar)
        sym_menu.add_checkbutton(label='Symmetry',
                                 onvalue=1,
                                 offvalue=0,
                                 variable=symmetry)
        self.menuBar.add_cascade(label='Symmetry', menu=sym_menu)
        


app = App()


SIZE = 15

