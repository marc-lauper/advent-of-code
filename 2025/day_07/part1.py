import re

USE_EXAMPLE = False
FILE = 'example.txt' if USE_EXAMPLE else  'input.txt'
TEMP_FiLE = 'temp.txt'

VERBOSE = FILE != 'input.txt'
DEBUG = FILE == 'example.txt'
RESULT = 0
GRID = []
START = 'S'
BEAM = '|'
SPLITTER = '^'

def print_verbose(text):
    if VERBOSE:
        print(text)
        

def print_debug(text):
    if DEBUG:
        print(text)

def find_start():
    for row in range(0, len(GRID)):
        for col in range(0, len(GRID[row])):
            if(GRID[row][col] == START):
                return row, col

def print_grid():
    print_verbose('################')
    for row in GRID:
        print_verbose(''.join(row))
    print_verbose('################')

with open(FILE, 'r') as file:
    for line in file:
        row = []
        for char in line:
            row.append(char)
        GRID.append(row)

    start_row, start_col = find_start()
    print_grid()
    print_debug(f'Start found at {start_row}, {start_col}')

    col_limit = len(GRID[0])-1

    for row in range(1, len(GRID)):
        for col in range(0, len(GRID[row])):
            if GRID[row-1][col] == START or GRID[row-1][col] == BEAM:
                if GRID[row][col] == SPLITTER:
                    if col > 0:
                        GRID[row][col-1] = BEAM
                    if col < col_limit:
                        GRID[row][col+1] = BEAM
                else:
                    GRID[row][col] = BEAM

    print_grid()

    for row in range(1, len(GRID)):
        for col in range(0, len(GRID[row])):
            if GRID[row][col] == SPLITTER:
                if GRID[row-1][col] == START or GRID[row-1][col] == BEAM:
                    RESULT += 1
    print (f"result: {RESULT}")
