import re, sys, os;
sys.setrecursionlimit(10**6)

VERBOSE = True
DEBUG = True
FILE = "input.txt"
maze = []
prices = []
path = []

if (FILE == "input.txt"):
    x_limit = 71
    y_limit = 71
    CORRUPTION = 1024
else:
    x_limit = 7
    y_limit = 7
    CORRUPTION = 12

start = (0,0)
end = (x_limit-1, y_limit-1)

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
WALL = '#'

PLAY_THE_TESTS = False

def print_verbose(text):
    if VERBOSE:
        print(text)

def print_debug(text):
    if DEBUG:
        print(text)

def do_some_tests():
    
    if not PLAY_THE_TESTS:
        return

# MOSTLY REUSING CODE FROM DAY 16...

def print_grid():
    global maze
    global prices

    if not (VERBOSE or PRINT_AS_CSV):
        return

    # else:
    for y in range(y_limit):
        for x in range(x_limit):
            symbol = maze[y][x]
            if (y, x) in path:
                print('*', end="")
            else:
                print(symbol, end="")
        print()

def get_next_position(current_position, direction):
    global x_limit
    global y_limit
    global maze

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
        return None

    return (y, x)

def get_price_to_move():
    return 1

def fill_maze(position):
    global maze
    global x_limit
    global y_limit

    for next_direction in [NORTH, EAST, SOUTH, WEST]:
        next_position = get_next_position(position, next_direction)
        if next_position == None:
            continue
        
        current_price = prices[position[0]][position[1]]
        current_price_for_next_position = prices[next_position[0]][next_position[1]]
        if current_price_for_next_position == None:
            current_price_for_next_position = sys.maxsize
        move_price = get_price_to_move()
        
        if move_price == None:
            continue
        
        new_price_for_next_position = current_price + move_price
        if new_price_for_next_position < current_price_for_next_position:
            prices[next_position[0]][next_position[1]] = new_price_for_next_position
            fill_maze(next_position)

with open(os.path.dirname(os.path.abspath(__file__)) + '/' + FILE, 'r') as file:
    result = 0

    # Some tests
    do_some_tests()

    for row in range(y_limit):
        maze.append([' '] * x_limit)
        prices.append([None] * x_limit)

    index = 0
    for line in file:
        line = line.replace('\n', '')
        if len(line) == 0:
            continue

        match = re.match(r"(\d+),(\d+)", line)
        if match:
            x = int(match.group(1))
            y = int(match.group(2))
            maze[y][x] = WALL
            
            index += 1
            if(index == CORRUPTION):
                break;
            else:
                continue

    prices[start[0]][start[1]] = 0
    fill_maze(start)
    print_grid()
    result = prices[end[0]][end[1]]

    print (f"\nresult: {result}")
