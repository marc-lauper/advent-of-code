import re;

USE_EXAMPLE = False
FILE = 'example.txt' if USE_EXAMPLE else  'input.txt'

VERBOSE = FILE != 'input.txt'
DEBUG = FILE == 'example.txt'

def print_verbose(text):
    if VERBOSE:
        print(text)
        

def print_debug(text):
    if DEBUG:
        print(text)

def count_neighbors(maze, h, w):
    count = 0
    height = len(maze)
    width = len(maze[0])
    
    if maze[h][w] != '@':
        return 999
    
    for dy in [-1, 0, 1]:
        ny = h + dy
        for dx in [-1, 0, 1]:
            if dy == 0 and dx == 0:
                continue
            nx = w + dx
            # print_debug(f"height: {height}, width: {width}, ny: {ny}, nx: {nx}")
            if 0 <= ny < height and 0 <= nx < width:
                if maze[ny][nx] == '@':
                    count += 1
    return count

maze = []
neighbors = []
with open(FILE, 'r') as file:
    result = 0
    
    for line in file:
        row = []
        for char in line:
            if char != '\n':
                row.append(char)
        maze.append(row)
    
    height = len(maze)
    width = len(maze[0])
    print_debug(f"maze[0] = {maze[0]}")
    
    for y in range(height):
        neighbors_row = []
        for x in range(width):
            neighbors_row.append(count_neighbors(maze, y, x))
        neighbors.append(neighbors_row)

    # How many neighbors are < 4?
    for y in range(height):
        for x in range(width):
            if neighbors[y][x] < 4:
                result += 1
                maze[y][x] = 'x'
    
    # print the maze
    for row in maze:
        print_verbose(''.join(row))
    
    print (f"result: {result}")
