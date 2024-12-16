import re;
import sys;
sys.setrecursionlimit(10**6)

VERBOSE = True
DEBUG = True
PRINT_AS_CSV = False
x_limit = 0
y_limit = 0
maze = []
prices = []
path = []
coming_from = []
start = (0, 0)
end = (0, 0)

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
WALL = '#'

PRICE_TO_MOVE = 1
PRICE_TO_TURN = 1000

def print_verbose(text):
    if VERBOSE:
        print(text)

def print_debug(text):
    if DEBUG:
        print(text)

def print_grid():
    global maze
    global prices

    if not (VERBOSE or PRINT_AS_CSV):
        return
    
    if PRINT_AS_CSV:
        for y in range(y_limit):
            first = True
            for x in range(x_limit):
                if first:
                    first = False
                else:
                    print(";", end="")
                symbol = maze[y][x]
                if (y, x) in path:
                    print(f"({prices[y][x]})", end="")
                else:
                    if symbol == '.':
                        print(f"{prices[y][x]}", end="")
                    else:
                        print(symbol, end="")
            print()

    else:
        for y in range(y_limit):
            for x in range(x_limit):
                symbol = maze[y][x]
                if (y, x) in path:
                    print('*', end="")
                elif symbol != WALL and prices[y][x] == sys.maxsize:
                    print('?', end="")
                else:
                    if symbol == '.':
                        symbol = ' ' # int(prices[y][x] / 10000)
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


def get_price_to_move(currently_facing, direction):
    global maze
    global x_limit
    global y_limit

    if currently_facing == direction:
        return PRICE_TO_MOVE

    diff = abs(direction - currently_facing)
    
    if diff % 2 == 1:
        return PRICE_TO_TURN + PRICE_TO_MOVE
    else:
        return None # Never go back

def fill_maze(position, facing):
    global maze
    global x_limit
    global y_limit

    for next_direction in [NORTH, EAST, SOUTH, WEST]:
        next_position = get_next_position(position, next_direction)
        if next_position == None:
            continue
        
        current_price = prices[position[0]][position[1]]
        current_price_for_next_position = prices[next_position[0]][next_position[1]]
        move_price = get_price_to_move(facing, next_direction)
        
        if move_price == None:
            continue
        
        new_price_for_next_position = current_price + move_price
        if new_price_for_next_position < current_price_for_next_position:
            prices[next_position[0]][next_position[1]] = new_price_for_next_position
            coming_from[next_position[0]][next_position[1]] = position
            fill_maze(next_position, next_direction)

def build_path():
    global coming_from
    global start
    global end
    
    p = []
    previous = coming_from[end[0]][end[1]]
    while previous != start:
        p.append(previous)
        previous = coming_from[previous[0]][previous[1]]
    return p

with open('example3.txt', 'r') as file:
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
        prices.append([sys.maxsize] * x_limit)
        coming_from.append([None] * x_limit)
        # Is one of the element the robot's position?
        if 'S' in line:
            start = (y_limit - 1, line.index('S'))
        if 'E' in line:
            end = (y_limit - 1, line.index('E'))

    prices[start[0]][start[1]] = 0

    print_debug(f"x_limit: {x_limit}, y_limit: {y_limit}")
    print_debug(f"start: {start}")
    print_debug(f"end: {end}")
    print_debug("")
    
    
    fill_maze(start, EAST)
    path = build_path()
    print_grid()
    result = prices[end[0]][end[1]]
    
    print (f"\nresult: {result}")


# 89464 is not correct (too high)
