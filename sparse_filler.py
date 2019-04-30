from collections import defaultdict
import re
from copy import deepcopy
from random import choice, shuffle

import numpy as np

from Grid_class import Grid

dic = defaultdict(list)
theme_words = defaultdict(list)

with open('clean_dictionary.txt', 'r') as f:
    for word in f.readlines():
        dic[len(word[:-1])].append(word[:-1]) #  remove trailing \n

with open('theme_words.txt', 'r') as f:
    for word in f.readlines():
        theme_words[len(word[:-1])].append(word[:-1]) #  remove trailing \n

with open('raw_grids.txt', 'r') as f:
    grids = [Grid(grid[:-1]) for grid in f.readlines()]


def grid_print(grid):
    for row in grid.grid:
        print(''.join(['\u2588' if c=='#' else c for c in row]))

def grid_stats(grid):
    stats = defaultdict(int)
    for pos in grid.positions:
        stats[pos.length] += 1
    return stats

def suitable_grid_finder(grids, theme_words):
    '''
    Find grids which have the most suitable number of positions for the
    theme words to go in. First naive attempt: One point for every position
    that matches a theme word, with no repeats.
    '''
    word_count = {key: len(theme_words[key]) for key in theme_words.keys()}
    scores = []
    for grid in grids:
        score = 0
        copy_count = dict(word_count)
        for pos in grid.positions:
            if pos.length in theme_words.keys() and \
               copy_count[pos.length]:
                copy_count[pos.length] -= 1
                score += 1
        scores.append((score, grid))
    return sorted(scores, key = lambda x: x[0], reverse = True)

def get_pattern(grid, pos):
    pattern = ''.join([c if c.isalpha() else '.' for c in grid[pos.slice]])
    return re.compile(pattern)

def check_arc_consistency(grid, position, word, dic):
    '''
    Check that all of the crossers of a suitable word are workable. Makes a
    copy, enters the word, and counts the matches.
    '''
    grid = grid.copy()
    grid[position.slice] = np.array(list(word)) #  put the word in the grid
    scores =  [get_freedom(grid, pos, dic) for pos in position.crossers]
    if all(scores):
        return sum(scores)
    return 0 #  If any crosser has no possible words we need to backtrack


def get_freedom(grid, position, dic):
    '''
    Find how many possible words fit in a single unfilled position
    '''
    pattern = get_pattern(grid, position)
    return sum([1 for word in dic[position.length]
                if re.match(pattern, word)])


def get_best_word(grid, position, theme_words):
    if position.length not in theme_words.keys():
        return
    pattern = get_pattern(grid.grid, position)
    possibles = [word for word in theme_words[position.length]
                 if re.match(pattern, word)]
    scores = [check_arc_consistency(grid.grid, position, word, dic)
              for word in possibles]
    combined = sorted(zip(scores, possibles), reverse=True)
    return [poss for score, poss in combined if score]

def grid_score(grid):
    return sum([1 for pos in grid.positions if pos.filled])

def theme_recursive(grid, position, theme_words, dic, depth = 0):
    depth += 1
    position.crossers.sort(reverse = True, key = lambda x: x.length)

    for pos in position.crossers:
        if pos.filled:
            continue
        best_word = get_best_word(grid, pos, theme_words)
        if not best_word:
            continue
        grid.enter_word(best_word[0], pos)
        theme_words[pos.length].remove(best_word[0]) #  Remove word from possibles
        grid, theme_words = theme_recursive(grid, pos, theme_words, dic, depth)
    return grid, theme_words #  No more matches, return grid in current form



def theme_fitter(grid, theme_words, dic):   
    theme_positions = [pos for pos in grid.positions
                 if pos.length in theme_words.keys()]
    theme_positions.sort(key = lambda x: x.length, reverse = True) #  long 1st

    for pos in theme_positions:
        if pos.filled:
            continue
        best_word = get_best_word(grid, pos, theme_words)
        if not best_word:
            continue
        grid.enter_word(best_word[0], pos)
        theme_words[pos.length].remove(best_word[0])
        grid, theme_words = theme_recursive(grid, pos, theme_words, dic)         
    
    return grid

def full_recursive(grid, positions, dic, depth = 0):
    depth += 1
    print(' '*depth, depth)

    for pos in positions:
        pattern = get_pattern(grid.grid, pos)
        possibles = [w for w in dic[pos.length] if re.match(pattern, w)]
        for poss in possibles:
            grid.enter_word(poss, pos)
            new_grid = full_recursive(grid, positions[1:], dic, depth)
            if new_grid:
                return new_grid
            grid.remove_word(pattern, pos)
        else:
            return
    return


        
def heur_recursive(grid, positions, dic, depth = 0):
    depth += 1
    print(' '*depth, depth)
    
    if not positions:
        return grid
    # Sort by most constrained
    positions.sort(key = lambda x: get_freedom(grid.grid, x, dic))

    for pos in positions:
        pattern = get_pattern(grid.grid, pos)
        possibles = get_best_word(grid, pos, dic)
        for poss in possibles:
            grid.enter_word(poss, pos)
            new_grid = heur_recursive(grid, positions[1:], dic, depth)
            if new_grid:
                return new_grid
            grid.remove_word(pattern, pos)
    return


best_grids =  suitable_grid_finder(grids, theme_words)
for key in theme_words.keys():
    shuffle(theme_words[key])

x = []
for _, grid in best_grids[:10]:
    grid = theme_fitter(grid, deepcopy(theme_words), dic)
    grid_print(grid)
    print("Score is: ", grid_score(grid))
    print("\n\n\n\n")
    x.append(grid)





        
