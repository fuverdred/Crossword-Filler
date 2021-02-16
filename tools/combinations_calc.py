from math import factorial
from collections import defaultdict

import numpy as np

from Puzzle_class import Puzzle

#### LOAD GRIDS AND WORDS #################################################
dic = defaultdict(list)
theme_dic = defaultdict(list)
light_dic = defaultdict(int)

with open('clean_dictionary.txt', 'r') as f:
    for word in f.readlines():
        dic[len(word[:-1])].append(word.strip('\n'))

with open('themes/chocolate_bars.txt', 'r') as f:
    for word in f.readlines():
        theme_dic[len(word[:-1])].append(word.strip('\n'))

with open('raw_grids.txt', 'r') as f:
    raw_grids = [grid[:-1] for grid in f.readlines()]

puzzles = [Puzzle(grid, dic) for grid in raw_grids]

puzzle = puzzles[18]
for pos in puzzle.positions:
    light_dic[pos.length] += 1
############################################################################

# == Theme dic stats ============
print('Theme dictionary stats')
N_theme_words = 0
fmt = '{:<6s} | {:>6s}'
print(fmt.format('Length', 'Count'))
print('-'*7 + '+' + '-'*7)
keys = sorted(theme_dic.keys())
for key in sorted(theme_dic.keys()):
    print(fmt.format(str(key), str(len(theme_dic[key]))))
    N_theme_words += key
print('-'*7 + '+' + '-'*7)
print(fmt.format('Total', str(N_theme_words)), end='\n\n')

# == Grid stats =================
print('Grid lights stats')
print(fmt.format('Length', 'Count'))
print('-'*7 + '+' + '-'*7)
for key in sorted(light_dic.keys()):
    print(fmt.format(str(key), str(light_dic[key])))

# == Removing irrelevant words and lengths ===

def nPr(n, r):
    return factorial(n) // factorial(n-r)

relevants = set(theme_dic.keys()).intersection(set(light_dic.keys()))

print('\nPossible combinations')
fmt = '{:<6s} | {:>6s} | {:>6s} | {:>6s}'
print(fmt.format('length', 'words', 'pos', 'combs'))
print('-'*7 + '+' + '-'*8 + '+' + '-'*8 + '+' + '-'*8)
total_combs = 1
for length in relevants:
    n_words = len(theme_dic[length])
    n_pos = light_dic[length]
    combs = 0
    for i in range(min(n_words, n_pos)+1):
        combs += nPr(max(n_words, n_pos), i)
        
    print(fmt.format(str(length),
                     str(n_words),
                     str(n_pos),
                     str(combs)))
    total_combs *= combs
print('-'*7 + '+' + '-'*8 + '+' + '-'*8 + '+' + '-'*8)
print('TOTAL  | {:d}'.format(total_combs))


