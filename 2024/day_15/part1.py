import re;

VERBOSE = False
DEBUG = False
x_limit = 0
y_limit = 0
warehouse = []
robot_position = (0, 0)
move_sequence = []
move_index = 0

EMPTY = '.'
WALL = '#'
BOX = 'O'
ROBOT = '@'

INCREASE_Y = 'v'
DECREASE_Y = '^'
INCREASE_X = '>'
DECREASE_X = '<'

def print_verbose(text):
    if VERBOSE:
        print(text)

def print_debug(text):
    if DEBUG:
        print(text)

def print_grid():
    global warehouse

    if not VERBOSE:
        return
    for y in range(y_limit):
        for x in range(x_limit):
            print(warehouse[y][x], end="")
        print()

def compute_result():
    global warehouse
    result = 0
    for y in range(y_limit):
        for x in range(x_limit):
            if warehouse[y][x] == BOX:
                result += 100*y + x
    return result

def push(starting_point, x_step, y_step):
    global warehouse
    item = warehouse[starting_point[0]][starting_point[1]]
    target = warehouse[starting_point[0]+y_step][starting_point[1] + x_step]
    if target == WALL:
        return False
    if target == EMPTY:
        warehouse[starting_point[0]+y_step][starting_point[1] + x_step] = item
        warehouse[starting_point[0]][starting_point[1]] = EMPTY
        return True
    if target == BOX or target == ROBOT:
        if push((starting_point[0]+y_step, starting_point[1] + x_step), x_step, y_step):
            warehouse[starting_point[0]+y_step][starting_point[1] + x_step] = item
            warehouse[starting_point[0]][starting_point[1]] = EMPTY
            return True
        return False
    
def step():
    global robot_position, move_index
    next_move = move_sequence[move_index]
    move_index += 1
    x_step = 1 if next_move == INCREASE_X else -1 if next_move == DECREASE_X else 0
    y_step = 1 if next_move == INCREASE_Y else -1 if next_move == DECREASE_Y else 0
    moved = push(robot_position, x_step, y_step)
    if moved:
        robot_position = (robot_position[0]+y_step, robot_position[1]+x_step)

with open('input.txt', 'r') as file:
    result = 0

    parsing_warehouse = True
    for line in file:
        line = line.replace('\n', '')
        if len(line) == 0:
            parsing_warehouse = False
            continue

        if parsing_warehouse:
            line = line.strip()
            warehouse.append(list(line))
            print_debug(f"line: {line}")
            x_limit = len(line)
            y_limit += 1
            # Is one of the element the robot's position?
            if '@' in line:
                robot_position = (line.index('@'), y_limit - 1)
        else:
            # concatenate move_sequence with the new line
            move_sequence.extend(list(line.strip()))

    print_debug(f"x_limit: {x_limit}, y_limit: {y_limit}")
    print_debug(f"warehouse: {warehouse}")
    print_debug(f"move_sequence: {move_sequence}")
    print_debug(f"robot_position: {robot_position}")
    
    print_verbose("Initial state:")
    print_grid()
    
    while move_index < len(move_sequence):
        move = move_sequence[move_index]
        print_verbose(f"Move {move}:")
        step()
        print_grid()
        print_verbose("")
    
    result = compute_result()

    print (f"\nresult: {result}")
