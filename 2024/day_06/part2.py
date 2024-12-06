# Note: the input data has been manually trimmed from its last empty line, to keep things simple
import re;
import time;

VERBOSE = False
DEBUG = False

visited = set()
current_position = (0, 0, 0) # row, column, direction (UP, DOWN, LEFT, RIGHT)
obstacles = []
row_limit = 0
column_limit = 0

def is_looping():
    global current_position
    while True:
        next_position_is_valid = False
        
        direction = current_position[2]
        while not next_position_is_valid:
            if direction == 0:
                next_position = (current_position[0] - 1, current_position[1], direction)
            elif direction == 1:
                next_position = (current_position[0], current_position[1] + 1, direction)
            elif direction == 2:
                next_position = (current_position[0] + 1, current_position[1], direction)
            elif direction == 3:
                next_position = (current_position[0], current_position[1] - 1, direction)
            else:
                print(f"Invalid direction {direction}")
                exit(1)
            
            if next_position[0] < 0 or next_position[0] == row_limit or next_position[1] < 0 or next_position[1] == column_limit:
                visited.add(current_position)
                # print_verbose(f"Out of bounds at {next_position}")
                # print_grid()
                return False
            
            if (next_position[0], next_position[1]) in obstacles:
                direction = (direction + 1) % 4
            elif next_position in visited:
                print_verbose(f"Loop detected at {next_position}")
                print_grid()
                return True
            else:
                next_position_is_valid = True
                visited.add(current_position)
                current_position = next_position
        
        print_debug(f"Moved to {current_position}")

def print_verbose(text):
    if VERBOSE:
        print(text)
        

def print_debug(text):
    if DEBUG:
        print(text)

def print_grid():
    if(not VERBOSE):
        return
    for row in range(0, row_limit):
        for column in range(0, column_limit):
            current_pos = (row, column)
            if obstacles.__contains__(current_pos):
                print("#", end="")
            elif visited.__contains__(current_pos):
                print("X", end="")
            else:
                print(".", end="")
        print()

with open('input.txt', 'r') as file:
    result = 0
    row = 0

    for line in file:
        if(len(line) < 2):
            continue
        
        column_limit = len(line)
        
        # The row is in form "   #   #      #", extract the position of every "#"
        for column in range(0, len(line)):
            if line[column] == "#":
                obstacles.append((row, column))
            elif line[column] == "^":
                current_position = (row, column, 0)
            elif line[column] == ">":
                current_position = (row, column, 1)
            elif line[column] == "v":
                current_position = (row, column, 2)
            elif line[column] == "<":
                current_position = (row, column, 3)
        row += 1

    row_limit = row
    original_position = current_position
    original_obstacles = obstacles.copy()
    is_looping()
    original_visited = []
    for item in visited:
        original_visited.append((item[0], item[1]))
    print_debug(f"Starting position is {current_position}")
    print_debug(f"Obstacles: {obstacles}")
    print_debug(f"Limits: {row_limit}x{column_limit}")

start_time = time.time()
for row in range(0, row_limit):
    for column in range(0, column_limit):
        progress_in_percent = (row * column_limit + column) / (row_limit * column_limit) * 100
        print(f"Row {row}/{row_limit}, column {column}/{column_limit} ({progress_in_percent:.2f}%)", end="\r")
        current_pos = (row, column)
        if not original_visited.__contains__(current_pos):
            print_debug(f"Position {current_pos} was not visited, skipping")
        elif obstacles.__contains__(current_pos):
            print_debug(f"Obstacle at {current_pos}, cannot put a new one here, skipping")
        elif original_position == current_pos:
            print_debug(f"Starting at {current_pos}, cannot put a new one here, skipping")
        else:
            obstacles = original_obstacles.copy()
            obstacles.append(current_pos)
            visited.clear()
            current_position = original_position
            print_verbose(f"Trying to put an obstacle at {current_pos}")
            if(is_looping()):
                print_verbose(f"Loop detected with obstacle at {current_pos}")
                result += 1

print()
print()
print(f"Result: {result}")