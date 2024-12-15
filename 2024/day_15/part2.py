import re;

VERBOSE = False
DEBUG = False
EXPAND = True
x_limit = 0
y_limit = 0
warehouse = []
robot_position = (0, 0)
move_sequence = []
move_index = 0

EMPTY = '.'
WALL = '#'
BOX = 'O'
BOX_LEFT = '['
BOX_RIGHT = ']'
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
            if warehouse[y][x] == BOX_LEFT:
                result += 100*y + x
    return result

def push_on_y(starting_point, y_step, move_it = False):
    global warehouse
    item = warehouse[starting_point[0]][starting_point[1]]
    target1 = warehouse[starting_point[0]+y_step][starting_point[1]]
    target2 = None
    item2 = None
    starting_point2 = None
    if item == BOX_LEFT:
        starting_point2 = (starting_point[0], starting_point[1] + 1)
    elif item == BOX_RIGHT:
        starting_point2 = (starting_point[0], starting_point[1] - 1)

    if starting_point2 != None:
        item2 = warehouse[starting_point2[0]][starting_point2[1]]
        target2 = warehouse[starting_point2[0] + y_step][starting_point2[1]]

    print_debug(f"push_on_y({starting_point}, {y_step}, {move_it})")
    print_debug(f"item: {item}, target1: {target1}, item2: {item2}, target2: {target2}")
    
    if target1 == WALL or target2 == WALL:
        return False
    
    if move_it:
        if target1 == BOX_LEFT or target1 == BOX_RIGHT or target1 == ROBOT:
            push_on_y((starting_point[0]+y_step, starting_point[1]), y_step, True)
        if starting_point2 != None:
            if target2 == BOX_LEFT or target2 == BOX_RIGHT or target2 == ROBOT:
                if item2 != target2:
                    push_on_y((starting_point2[0]+y_step, starting_point2[1]), y_step, True)
            warehouse[starting_point2[0]+y_step][starting_point2[1]] = item2
            warehouse[starting_point2[0]][starting_point2[1]] = EMPTY
        warehouse[starting_point[0]+y_step][starting_point[1]] = item
        warehouse[starting_point[0]][starting_point[1]] = EMPTY

    else:
        result = True
        if target1 == BOX_LEFT or target1 == BOX_RIGHT or target1 == ROBOT:
            result = result and push_on_y((starting_point[0]+y_step, starting_point[1]), y_step)
        if starting_point2 != None and (target2 == BOX_LEFT or target2 == BOX_RIGHT or target2 == ROBOT):
            result = result and push_on_y((starting_point2[0]+y_step, starting_point2[1]), y_step)
        return result

def push_on_x(starting_point, x_step):
    global warehouse
    item = warehouse[starting_point[0]][starting_point[1]]
    target = warehouse[starting_point[0]][starting_point[1] + x_step]
    if target == WALL:
        return False
    if target == EMPTY:
        warehouse[starting_point[0]][starting_point[1] + x_step] = item
        warehouse[starting_point[0]][starting_point[1]] = EMPTY
        return True
    if target == BOX_LEFT or target == BOX_RIGHT or target == ROBOT:
        if push_on_x((starting_point[0], starting_point[1] + x_step), x_step):
            warehouse[starting_point[0]][starting_point[1] + x_step] = item
            warehouse[starting_point[0]][starting_point[1]] = EMPTY
            return True
        return False
    
def step():
    global robot_position, move_index
    next_move = move_sequence[move_index]
    move_index += 1
    x_step = 1 if next_move == INCREASE_X else -1 if next_move == DECREASE_X else 0
    y_step = 1 if next_move == INCREASE_Y else -1 if next_move == DECREASE_Y else 0
    
    if x_step != 0:
        moved = push_on_x(robot_position, x_step)
        if moved:
            robot_position = (robot_position[0]+y_step, robot_position[1]+x_step)
    else:
        can_move = push_on_y(robot_position, y_step, False)
        if can_move:
            push_on_y(robot_position, y_step, True)
            robot_position = (robot_position[0]+y_step, robot_position[1])

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
            if EXPAND:
                line = line.replace(EMPTY, f"{EMPTY}{EMPTY}")
                line = line.replace(WALL, f"{WALL}{WALL}")
                line = line.replace(BOX, f"{BOX_LEFT}{BOX_RIGHT}")
                line = line.replace(ROBOT, f"{ROBOT}{EMPTY}")
            warehouse.append(list(line))
            x_limit = len(line)
            y_limit += 1
            # Is one of the element the robot's position?
            if '@' in line:
                robot_position = (y_limit - 1, line.index('@'))
        else:
            # concatenate move_sequence with the new line
            move_sequence.extend(list(line.strip()))

    print_verbose("Initial state:")
    print_grid()
    print_verbose("")
    
    while move_index < len(move_sequence):
        move = move_sequence[move_index]
        print_verbose(f"Move {move}:")
        step()
        print_grid()
        print_verbose("")
    
    result = compute_result()

    print (f"\nresult: {result}")
