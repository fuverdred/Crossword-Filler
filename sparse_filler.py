from collections import defaultdict
import re
from copy import deepcopy
from random import choice, shuffle

import numpy as np

from Grid_class import Puzzle

##dic = defaultdict(list)
##theme_words = defaultdict(list)
##
##with open('clean_dictionary.txt', 'r') as f:
##    for word in f.readlines():
##        dic[len(word[:-1])].append(word[:-1]) #  remove trailing \n
##
##with open('themes/chocolate_bars.txt', 'r') as f:
##    for word in f.readlines():
##        theme_words[len(word[:-1])].append(word[:-1]) #  remove trailing \n
##
##with open('raw_grids.txt', 'r') as f:
##    puzzles = [Puzzle(grid[:-1]) for grid in f.readlines()]


def grid_print(puzzle):
    for row in puzzle.grid:
        print(''.join(['\u2588' if c=='#' else c for c in row]))


def suitable_grid_finder(puzzles, theme_words):
    '''
    Find grids which have the most suitable number of positions for the
    theme words to go in. First naive attempt: One point for every position
    that matches a theme word, with no repeats.
    '''
    word_count = {key: len(theme_words[key]) for key in theme_words.keys()}
    scores = []
    for puzzle in puzzles:
        score = 0
        copy_count = dict(word_count)
        for pos in puzzle.positions:
            if pos.length in theme_words.keys() and \
               copy_count[pos.length]:
                copy_count[pos.length] -= 1
                score += 1
        scores.append((score, puzzle))
    return sorted(scores, key=lambda x: x[0], reverse=True)

def get_pattern(grid, pos): #  Expects a numpy array in
    pattern = ''.join([c if c.isalpha() else '.' 
                       for c in grid[pos.slice]])
    return re.compile(pattern)

def check_arc_consistency(grid, position, word, dic): #  Expects numpy array
    '''
    Check that all of the crossers of a suitable word are workable. Makes a
    copy, enters the word, and counts the matches.
    '''
    if all([pos.filled for pos in position.crossers]):
        return 1 #  Arc consistency doesn't matter
    grid = grid.copy() #  New copy in memory
    grid[position.slice] = np.array(list(word)) #  put the word in the grid
    scores =  [get_freedom(grid, pos, dic) for pos in position.crossers
               if not pos.filled]
    if all(scores):
        return sum(scores)
    return 0 #  If any crosser has no possible words we need to backtrack


def get_freedom(grid, position, dic): #  Expects a numpy array
    '''
    Find how many possible words fit in a single unfilled position
    '''
    pattern = get_pattern(grid, position)
    return sum([1 for word in dic[position.length]
                if re.match(pattern, word)])


def get_possible_words(grid, position, dic): #  Expects a numpy array
    pattern = get_pattern(grid, position)
    return [word for word in dic[position.length] if re.match(pattern, word)]

def get_best_words(grid, position, dic, full_dic): #  Expects numpy array
    '''
    Function for filling positions with unfilled crossers. All possible words
    for the position are found, and then ranked according to how much they
    constrain the crossers
    '''
    if position.length not in dic.keys(): #  only relevant for themed words
        return
    possibles = get_possible_words(grid, position, dic)
    if not possibles:
        return #  dead end
    scores = [check_arc_consistency(grid, position, word, full_dic)
              for word in possibles]
    combined = sorted(zip(scores, possibles), reverse=True)
    return [poss for score, poss in combined if score]


def theme_recursive(puzzle, position, theme_words, dic, depth = 0):
    depth += 1
    position.crossers.sort(reverse=True, key=lambda x: x.length)

    for pos in position.crossers:
        if pos.filled:
            continue
        best_word = get_best_words(puzzle.grid, pos, theme_words, dic)
        if not best_word:
            continue
        puzzle.enter_word(best_word[0], pos)
        theme_words[pos.length].remove(best_word[0]) #  Remove word from possibles
        puzzle, theme_words = theme_recursive(puzzle, pos, theme_words, dic, depth)
    return puzzle, theme_words #  No more matches, return grid in current form



def theme_fitter(puzzle, theme_words, dic):   
    theme_positions = [pos for pos in puzzle.positions
                 if pos.length in theme_words.keys()]
    theme_positions.sort(key=lambda x: x.length, reverse=True) #  longest 1st

    for pos in theme_positions:
        if pos.filled:
            continue
        best_word = get_best_words(puzzle.grid, pos, theme_words, dic)
        if not best_word:
            continue
        puzzle.enter_word(best_word[0], pos)
        theme_words[pos.length].remove(best_word[0])
        puzzle, theme_words = theme_recursive(puzzle, pos, theme_words, dic)         
    
    return puzzle


def recursive(puzzle, depth = 0):
    depth += 1
    print(depth*' ', depth)
    
    if not puzzle.unfilled: # Puzzle complete
        return puzzle

    #sort positions by most constrained
    puzzle.unfilled.sort(key = lambda x: get_freedom(puzzle.grid, x, dic))

    for poss in get_best_words(puzzle.grid, puzzle.unfilled[0], dic, dic)[:20]:
        pattern = get_pattern(puzzle.grid, puzzle.unfilled[0])
        grid_print(puzzle)
        print('\n'*2)
        puzzle.enter_word(poss, puzzle.unfilled[0])
        new_puzzle = recursive(puzzle, depth)
        if new_puzzle:
            return new_puzzle
        puzzle.remove_word(pattern, puzzle.unfilled[0])
    return #  Back track


##for i in range(3,16):
##    shuffle(dic[i])
##
##poss_grids = []
##for puzzle in puzzles:
##    x = theme_fitter(puzzle, deepcopy(theme_words), dic)
##    print("Score: ", len(puzzle.positions) - len(puzzle.unfilled), '\n'*2)
##    poss_grids.append((len(puzzle.positions) - len(puzzle.unfilled), x))



        
