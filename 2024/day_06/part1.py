# Note: the input data has been manually trimmed from its last empty line, to keep things simple
import re;

VERBOSE = True
DEBUG = True

visited = set()
current_position = (0, 0)
obstacles = []
row_limit = 0
column_limit = 0
direction = 0 # 0: UP, 1: RIGHT, 2: DOWN, 3: LEFT

def move():
    global current_position
    global direction
    next_position_is_valid = False
    
    while not next_position_is_valid:
        if direction == 0:
            next_position = (current_position[0] - 1, current_position[1])
        elif direction == 1:
            next_position = (current_position[0], current_position[1] + 1)
        elif direction == 2:
            next_position = (current_position[0] + 1, current_position[1])
        elif direction == 3:
            next_position = (current_position[0], current_position[1] - 1)
        else:
            print(f"Invalid direction {direction}")
            exit(1)
        
        if next_position[0] < 0 or next_position[0] == row_limit or next_position[1] < 0 or next_position[1] == column_limit:
            visited.add(current_position)
            print(f"Visited {visited}")
            print_grid()
            print(f"Result: {len(visited)}")
            quit()
        
        if next_position in obstacles:
            direction = (direction + 1) % 4
        else:
            next_position_is_valid = True
            visited.add(current_position)
            current_position = next_position
        
    print_verbose(f"Moved to {current_position}")

def print_verbose(text):
    if VERBOSE:
        print(text)
        

def print_debug(text):
    if DEBUG:
        print(text)

def print_grid():
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
                current_position = (row, column)
                direction = 0
            elif line[column] == ">":
                current_position = (row, column)
                direction = 1
            elif line[column] == "v":
                current_position = (row, column)
                direction = 2
            elif line[column] == "<":
                current_position = (row, column)
                direction = 3
        row += 1

    row_limit = row
    print_debug(f"Starting position is {current_position}, direction is {direction}")
    print_debug(f"Obstacles: {obstacles}")
    print_debug(f"Limits: {row_limit}x{column_limit}")
    
    while True:
        move()
