USE_EXAMPLE = False
FILE = 'example.txt' if USE_EXAMPLE else  'input.txt'

VERBOSE = FILE != 'input.txt'
DEBUG = FILE == 'example.txt'
HEIGHT = -1
WIDTH = -1
RESULT = 0
MAZE = []
NEIGHBORS = []

def print_verbose(text):
    if VERBOSE:
        print(text)
        

def print_debug(text):
    if DEBUG:
        print(text)

def count_neighbors(h, w):
    global MAZE, HEIGHT, WIDTH
    count = 0
    
    if MAZE[h][w] != '@':
        return 999
    
    for dy in [-1, 0, 1]:
        ny = h + dy
        for dx in [-1, 0, 1]:
            if dy == 0 and dx == 0:
                continue
            nx = w + dx
            if 0 <= ny < HEIGHT and 0 <= nx < WIDTH:
                if MAZE[ny][nx] == '@':
                    count += 1
    return count

def remove_if_possible(h, w):
    global MAZE, HEIGHT, WIDTH, NEIGHBORS, RESULT
    if h < 0 or h >= HEIGHT or w < 0 or w >= WIDTH:
        return False

    if MAZE[h][w] != '@':
        return False

    if NEIGHBORS[h][w] >= 4:
        return False
    
    MAZE[h][w] = 'X'
    RESULT += 1

    for dy in [-1, 0, 1]:
        ny = h + dy
        for dx in [-1, 0, 1]:
            if dy == 0 and dx == 0:
                continue
            nx = w + dx
            if 0 <= ny < HEIGHT and 0 <= nx < WIDTH:
                NEIGHBORS[ny][nx] = NEIGHBORS[ny][nx] - 1

    for dy in [-1, 0, 1]:
        ny = h + dy
        for dx in [-1, 0, 1]:
            if dy == 0 and dx == 0:
                continue
            nx = w + dx
            remove_if_possible(ny, nx)

with open(FILE, 'r') as file:
    
    for line in file:
        row = []
        for char in line:
            if char != '\n':
                row.append(char)
        MAZE.append(row)
    
    HEIGHT = len(MAZE)
    WIDTH = len(MAZE[0])
    print_debug(f"maze[0] = {MAZE[0]}")
    
    for y in range(HEIGHT):
        neighbors_row = []
        for x in range(WIDTH):
            neighbors_row.append(count_neighbors(y, x))
        NEIGHBORS.append(neighbors_row)

    for y in range(HEIGHT):
        neighbors_row = []
        for x in range(WIDTH):
            remove_if_possible(y, x)
    
    for row in MAZE:
        print_verbose(''.join(row))
    
    print (f"result: {RESULT}")
