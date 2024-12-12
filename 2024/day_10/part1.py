import re;
from functools import cmp_to_key;

VERBOSE = True
DEBUG = True
array = []
trails = {}

def print_verbose(text):
    if VERBOSE:
        print(text)

def print_debug(text):
    if DEBUG:
        print(text)

def find_trails(start_position, next_position, current_trail = ""):
    global array
    global trails
    
    if next_position[0] < 0 or next_position[0] >= len(array) or next_position[1] < 0 or next_position[1] >= len(array[0]):
        return
    
    if current_trail == "":
        last_step = -1
    else:
        last_step = int(current_trail[-1])
    current_step = int(array[next_position[0]][next_position[1]])
    
    if current_step != last_step + 1:
        return
    
    current_trail += str(current_step)
    print_debug(f"   [{next_position}] current_trail: {current_trail}")
    
    if current_step == 9:
        print_verbose(f"[{start_position}] Found trail {current_trail}")
        trails[start_position].add(next_position)
        return
    
    find_trails(start_position, (next_position[0] - 1, next_position[1]), current_trail)
    find_trails(start_position, (next_position[0], next_position[1] + 1), current_trail)
    find_trails(start_position, (next_position[0] + 1, next_position[1]), current_trail)
    find_trails(start_position, (next_position[0], next_position[1] - 1), current_trail)

with open('input.txt', 'r') as file:
    result = 0
    starting_row = 0

    # Build a two-dimension array based on the content of the file
    array = []
    for line in file:
        array.append(list(line.strip()))
        for starting_column in range(0, len(array[starting_row])):
            if array[starting_row][starting_column] == "0":
                trails[(starting_row, starting_column)] = set()
        starting_row += 1

    for key in trails.keys():
        find_trails(key, key)

    for key in trails.keys():
        print_verbose(f"[{key}] trails: {len(trails[key])}")
        result += len(trails[key])

    print (f"\nresult: {result}")
