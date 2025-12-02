import re, sys, os;
sys.setrecursionlimit(10**6)

VERBOSE = True
DEBUG = True
FILE = "input.txt"
maze = []
adjacents = []
cheats = {}
x_limit = 0
y_limit = 0
start = (0, 0)
end = (0, 0)

if(FILE == "example.txt"):
    cheat_limit = 0
else:
    cheat_limit = 100

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
WALL = '#'
PATH = '0'

def print_verbose(text):
    if VERBOSE:
        print(text)

def print_debug(text):
    if DEBUG:
        print(text)

def print_grid():
    global maze

    if not (VERBOSE or PRINT_AS_CSV):
        return

    # else:
    for y in range(y_limit):
        for x in range(x_limit):
            symbol = maze[y][x]
            print(symbol, end="")
        print()

def get_next_position(current_position, direction, step):
    global x_limit
    global y_limit
    global maze
    global adjacents
    global cheats

    y = current_position[0]
    x = current_position[1]

    if direction == NORTH:
        y -= 1
    elif direction == EAST:
        x += 1
    elif direction == SOUTH:
        y += 1
    elif direction == WEST:
        x -= 1

    if x < 0 or x >= x_limit or y < 0 or y >= y_limit:
        return None
    
    if (maze[y][x] == WALL):
        if(adjacents[y][x] == None):
            adjacents[y][x] = []
        else:
            for adjacent in adjacents[y][x]:
                cheat = abs(step - adjacent) - 2
                if cheat > 0:
                    if cheat not in cheats:
                        cheats[cheat] = 1
                    else:
                        cheats[cheat] += 1
                    print_debug(f"Found a cheat between step {step} and {adjacent}, saving {cheat} picoseconds")
        adjacents[y][x].append(step)
        return None

    if (maze[y][x] == PATH):
        return None

    return (y, x)

def get_price_to_move():
    return 1

def fill_maze(position, step = 0):
    global maze
    global x_limit
    global y_limit

    maze[position[0]][position[1]] = PATH

    for next_direction in [NORTH, EAST, SOUTH, WEST]:
        next_position = get_next_position(position, next_direction, step)
        if next_position != None:
            fill_maze(next_position, step + 1)

with open(os.path.dirname(os.path.abspath(__file__)) + '/' + FILE, 'r') as file:
    result = 0

    for line in file:
        line = line.replace('\n', '')
        if len(line) == 0:
            continue

        line = line.strip()
        maze.append(list(line))
        print_debug(f"line: {line}")
        x_limit = len(line)
        y_limit += 1
        if 'S' in line:
            start = (y_limit - 1, line.index('S'))
        if 'E' in line:
            end = (y_limit - 1, line.index('E'))
        adjacents.append([None] * x_limit)

    fill_maze(start)
    print_grid()

    # list the number of cheats, sorted by the number of picoseconds
    for cheat in sorted(cheats.keys()):
        if(cheat >= cheat_limit):
            print(f"There are {cheats[cheat]} cheats that save {cheat} picoseconds.")
            result += cheats[cheat]

    print (f"\nresult: {result}")
