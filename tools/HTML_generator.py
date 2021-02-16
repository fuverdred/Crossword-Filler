'''
In raw_gids.txt light squares are indicated by spaces, dark squares by #

Output each grid into HTML with the following CSS:

'''

with open('raw_grids.txt') as f:
    raw_grids = [grid.strip('\n') for grid in f.readlines()]

LIGHT = '<td><div class="xw_light"></div></td>'
DARK = '<td><div class="xw_dark"></div></td>'

translator = {' ': LIGHT,
              '#': DARK}

def grid_row(raw, indent=0):
    row = [' '*indent + '<tr>']
    for char in raw:
        row.append(' '*(indent+2) + translator[char])
    row.append(' '*indent + '</tr>')
    return '\n'.join(row)

def print_html_grid(grid):
    grid_html = ['<table class="xw_grid">']
    for i in range(0, len(grid), int(len(grid)**0.5)):
        grid_html.append(grid_row(grid[i:i+15], indent=2))
    grid_html.append(('</table>'))
    return '\n'.join(grid_html)
