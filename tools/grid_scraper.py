from bs4 import BeautifulSoup

import requests

url = "https://www.theguardian.com/crosswords/cryptic/27558"

r = requests.get(url)

soup = BeautifulSoup(r.content, "html.parser")

grid = list(soup.find(class_ = "crossword__grid"))

def make_grid(grid, l=15):
    return [['#' if grid[i+(l*j)] is "#" else " " for i in range(l)]
            for j in range(l)]

def grid_print(grid, l=15):
    for i in range(l):
        print(''.join(grid[i]))



unique_grids = []

for i in range(27000,27560):
    if i == 26330:
        continue
    url = "https://www.theguardian.com/crosswords/cryptic/"+str(i)
    print(url)
    r = requests.get(url)
    if not r:
        continue
    soup = BeautifulSoup(r.content, "html.parser")

    grid = list(soup.find(class_ = "crossword__grid"))

    blank = [['#' for i in range(15)] for j in range(15)]

    for sq in grid[3:-1]:
        try:
            x = int(float(sq.rect['x']))//32
            y = int(float(sq.rect['y']))//32
        except TypeError:
            x = int(float(sq['x']))//32
            y = int(float(sq['y']))//32
        blank[y][x] = ' '
    grid = ''.join([c for row in blank for c in row])
    if grid not in unique_grids:
        unique_grids.append(grid)
        grid_print(make_grid(grid))
print("\n\n")
