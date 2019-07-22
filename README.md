# Themed Crossword Maker
A crossword creator aimed at making themed grids (English style crossword)

From a small list of themed words (<< entire dictionary) fit as many words as possible into a grid, 
while maintaining arc consistency. Arc consistency means the grid can still be filled with other, non-
themed words. Bear in mind that there will also be an optimal grid or grids for any given choice
of theme words.

## Quick glossary of terms:
- **Grid** : The collection of blanks spaces where letters can go and dividers where they can't. Here
  we will only deal with square grids, although it should be easily modifiable for any shape.
- **Position** : This is a location on the grid where a whole word can go. Recorded in the form
  (i, j, length, direction), where i and j are row and column.
- **Crosser** : Any position which intersects with another position.
- **Arc Consistency** : The grid is arc consistent if no position is blocked. Any word which leads
  to a blocked position is not arc consistent and needs to be removed. Along side this is the idea
  of a propagation score for a word. The most basic way to calculate this is to count the number
  of possible crossers for the word if it were entered into a position.

## Heuristic strategy for theme fitting
1. Only positions for which the correct word length exists in the themed dic are considered, and
   vice versa.
2. The first position in the list is chosen, and the possible theme words are ranked based on
   how they affect the freedom of the grid, highest freedom first. This word is then entered
   into the grid and the weak recursive function is called. If there are no arc consistent words, 
   move onto the next position.
3. Weakly recursively search for crossers in the last position entered, if one exists, continue
   the recursion. If multiple exist, the one with the most freedom is chosen, there is no back
   tracking to replace words, hence I have called it weak recursion. It will however try other
   words in other crossers.
4. Repeat the steps 2 and 3 until no positions or theme words are left.

## GUI
The GUI is intended to be used to fill the grid after it has been fitted with as many themed words
as possible. This could also be done using a similar method to the heuristic strategy above, but
with more back tracking, possibly removing the theme word leading to the least freedom if the
grid cannot be filled. However, the dictionary used is very large, and has many very unconventional
words which would make for a bad crossword.

![GUI_example](https://github.com/fuverdred/Crossword-Filler/blob/master/Example.PNG?raw=true)

Instead the grid is colour coded showing the freedom of positions, allowing the setter to fill the
positions with the least freedom first, from the range of words which fit the possible position.
The list of words is ranked by their propagation score, which is also listed alongside, meaning that
a word can be ranked on its prevalence or interest instead of just score.


#### Notes
[lru cache optimsation](https://docs.python.org/3/library/functools.html#functools.lru_cache)
[integer programming](https://stmorse.github.io/journal/IP-Crossword-puzzles.html)
[python wrapper on US style](https://github.com/jsgonsette/Wizium)
