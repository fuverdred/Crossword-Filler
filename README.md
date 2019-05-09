#Themed Crossword Maker
A crossword creator aimed at making themed grids (English style crossword)

From a small list of themed words (<< entire dictionary) fit as many words as possible into a grid, 
while maintaining arc consistency. Arc consistency means the grid can still be filled with other, non-
themed words. Bear in mind that there will also be an optimal grid or grids for any given choice
of theme words.

##Quick glossary of terms:
- Grid : The collection of blanks spaces where letters can go and dividers where they can't. Here
  we will only deal with square grids, although it should be easily modifiable for any shape.
- Position : This is a location on the grid where a whole word can go. Recorded in the form
  (i, j, length, direction), where i and j are row and column.
- Crosser : Any position which intersects with another position.

##Heuristic strategy for theme fitting
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
4. Repeat the previous steps until no positions or theme words are left.


![GUI_example](https://github.com/fuverdred/Crossword-Filler/blob/master/Example.PNG?raw=true)
