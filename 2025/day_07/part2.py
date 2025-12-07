from functools import cache

USE_EXAMPLE = False
FILE = 'example.txt' if USE_EXAMPLE else  'input.txt'
TEMP_FiLE = 'temp.txt'

VERBOSE = FILE != 'input.txt'
DEBUG = FILE == 'example.txt'
RESULT = 0
GRID = []
INSTANCES = []
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

@cache
def find_instances(row, col):
    col_limit = len(GRID[0])-1
    for r in range(row+1, len(INSTANCES)):
        if INSTANCES[r][col] > 0:
            return INSTANCES[r][col]
        if GRID[r][col] == SPLITTER:
            INSTANCES[r][col] = 0
            if col > 0:
                INSTANCES[r][col] += find_instances(r, col-1)
            if col < col_limit:
                INSTANCES[r][col] += find_instances(r, col+1)
            return INSTANCES[r][col]
    return 1

with open(FILE, 'r') as file:
    for line in file:
        row = []
        instances_row = []
        for char in line:
            row.append(char)
            instances_row.append(0)
        GRID.append(row)
        INSTANCES.append(instances_row)

    start_row, start_col = find_start()
    print_grid()
    print_debug(f'Start found at {start_row}, {start_col}')

    print_grid()

    RESULT = find_instances(start_row, start_col)
    print (f"result: {RESULT}")
