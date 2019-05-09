A crossword creator aimed at making themed grids (English style crossword)

From a small list of themed words (<< entire dictionary) fit as many words as possible into a grid, 
while maintaining arc consistency. Arc consistency means the grid can still be filled with other, non-
themed words. Bear in mind that there will also be an optimal grid or grids for any given choice
of theme words.

Quick glossary of terms:
- Grid : The collection of blanks spaces where letters can go and dividers where they can't. Here
  we will only deal with square grids, although it should be easily modifiable for any shape.
- Position : This is a location on the grid where a whole word can go. Recorded in the form
  (i, j, length, direction), where i and j are row and column as usual.
- Crosser : Any position which intersects with another position.

Strategy:
1. First find the top N grids which are suitable for the chosen theme words. The current naive
   method uses a simple count of positions lengths matching word lengths, with no repetition
   allowed.
2. Fill in the longest themed word first. If there are multiple longest themed words fill in
   the least constrained first. Again this uses a naive approach. For each of the possible
   longest themed words count the number of suitable crossers from the large dictionary. Highest
   count is entered into the position.
3. Sort the crossers of this word


Strategy:
The strategy breaks into three modes: Fresh positions for themed words, finding theme words
which intersect with any already placed theme word and filling the rest the spaces with any
old word. We will need to switch between these modes as the grid is filled out, with back tracking
between them.

1. Fill in the longest themed word first. If there are multiple longest themed words fill in
   the least constrained first. This uses a naive approach, for each of the possible
   longest themed words count the number of suitable crossers from the large dictionary. Highest
   count is entered into the position.
   
Almost full recursive theme fitter:

There are two ways we can reach the limit of recursion:
1. Run out of all theme words.
2. Run out of positions to fit any themed word. E.g if there are only 2 positions on the grid of
   length 4 but we have 3 or more 4 letter themed words.
3. Some combination of the above. E.g. there are only 4 letter theme words left, but only 5
   letter positions available.
   
GUI
![GUI_example](fuverdred.github.com/Crossword-Filler/Example.png)
