import os;
import sys;
sys.setrecursionlimit(10**6)

VERBOSE = True
DEBUG = True
x_limit = 0
y_limit = 0
maze = []
prices = []
path = []
start = (0, 0)
end = (0, 0)

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
WALL = '#'
OPTIMAL_PATH = '0'

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

    # else:
    for y in range(y_limit):
        for x in range(x_limit):
            symbol = maze[y][x]
            if (y, x) in path:
                print('*', end="")
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
        
        if prices[position[0]][position[1]] == None:
            prices[position[0]][position[1]] = [None, None, None, None]
        if prices[next_position[0]][next_position[1]] == None:
            prices[next_position[0]][next_position[1]] = [None, None, None, None]

        current_price = prices[position[0]][position[1]][facing]
        current_price_for_next_position = prices[next_position[0]][next_position[1]][next_direction]
        if current_price_for_next_position == None:
            current_price_for_next_position = sys.maxsize
        move_price = get_price_to_move(facing, next_direction)
        
        if move_price == None:
            continue
        
        new_price_for_next_position = current_price + move_price
        if new_price_for_next_position < current_price_for_next_position:
            prices[next_position[0]][next_position[1]][next_direction] = new_price_for_next_position
            fill_maze(next_position, next_direction)

def smallest_of(array_with_int_and_none):
    smallest = sys.maxsize
    for i in range(len(array_with_int_and_none)):
        if array_with_int_and_none[i] != None and array_with_int_and_none[i] < smallest:
            smallest = array_with_int_and_none[i]
    return smallest

def index_of_smallest(array_with_int_and_none):
    smallest = sys.maxsize
    index = -1
    for i in range(len(array_with_int_and_none)):
        if array_with_int_and_none[i] != None and array_with_int_and_none[i] < smallest:
            smallest = array_with_int_and_none[i]
            index = i
    return index

def invert_direction(direction):
    return (direction + 2) % 4

def fill_optimal_path(current_position = None, current_price = None, current_direction = None):
    global mage
    global prices
    global end
    
    if current_position == None:
        current_position = end
        current_price = smallest_of(prices[end[0]][end[1]])+1
        current_direction = index_of_smallest(prices[end[0]][end[1]])
        maze[end[0]][end[1]] = OPTIMAL_PATH
        maze[start[0]][start[1]] = OPTIMAL_PATH
    
    for incoming_direction in [NORTH, EAST, SOUTH, WEST]:
        next_price = prices[current_position[0]][current_position[1]][incoming_direction]
        if next_price == None:
            continue
        compare_price = next_price
        if incoming_direction != current_direction:
            compare_price += PRICE_TO_TURN
        if compare_price < current_price:
            next_position = get_next_position(current_position, invert_direction(incoming_direction))
            if maze[next_position[0]][next_position[1]] != OPTIMAL_PATH:
                maze[next_position[0]][next_position[1]] = OPTIMAL_PATH
                fill_optimal_path(next_position, next_price, incoming_direction)

def count_optimal_path():
    global maze
    count = 0
    for y in range(y_limit):
        for x in range(x_limit):
            if maze[y][x] == OPTIMAL_PATH:
                count += 1
    return count

with open(os.path.dirname(os.path.abspath(__file__)) + '/input.txt', 'r') as file:
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
        prices.append([None] * x_limit)
        if 'S' in line:
            start = (y_limit - 1, line.index('S'))
        if 'E' in line:
            end = (y_limit - 1, line.index('E'))

    prices[start[0]][start[1]] = [0, 0, 0, 0]

    print_debug(f"x_limit: {x_limit}, y_limit: {y_limit}")
    print_debug(f"start: {start}")
    print_debug(f"end: {end}")
    print_debug("")
    
    fill_maze(start, EAST)
    print_grid()
    possible_results = prices[end[0]][end[1]]
    result = smallest_of(possible_results)
    print (f"\nresult of part 1: {result}")

    fill_optimal_path()
    result = count_optimal_path()
    print_grid()
    
    print (f"\nresult of aprt 2: {result}")