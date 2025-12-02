import re;

LIMIT = 100

VERBOSE = True
DEBUG = False

def print_verbose(text):
    if VERBOSE:
        print(text)
        

def print_debug(text):
    if DEBUG:
        print(text)

with open('input.txt', 'r') as file:
    position = 50
    result = 0
    
    for line in file:
        values = re.findall(r'([LR])(\d+)', line)[0]
        print_debug(f"values: {values}")
        direction = values[0]
        distance = int(values[1])
        if direction == 'L':
            position -= distance
        elif direction == 'R':
            position += distance
        while position < 0:
            position += LIMIT
        while position >= LIMIT:
            position -= LIMIT
        
        print_verbose(f"position: {position}")
        if position == 0:
            result += 1
    
    print (f"result: {result}")
