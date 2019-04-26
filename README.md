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
1. Fill in the position with the most crossers, practically this is the longest position that has
   a themed word of the same length.
2. ???
3. Profit
