import re

USE_EXAMPLE = False
FILE = 'example.txt' if USE_EXAMPLE else  'input.txt'
TEMP_FiLE = 'temp.txt'

VERBOSE = FILE != 'input.txt'
DEBUG = FILE == 'example.txt'
RESULT = 0
ROWS = []
OPERATIONS = []

def print_verbose(text):
    if VERBOSE:
        print(text)
        

def print_debug(text):
    if DEBUG:
        print(text)

with open(FILE, 'r') as file:
    
    # Read the file and rotate it clockwise once (keeping spaces intact)
    lines = file.readlines()
    max_length = max(len(line.rstrip('\n')) for line in lines)
    rotated_lines = []
    for col in range(max_length):
        new_line = ''
        for row in reversed(range(len(lines))):
            if col < len(lines[row]):
                new_line += lines[row][col]
            else:
                new_line += ' '
        rotated_lines.append(new_line.rstrip())

    # Write the rotated lines to a temporary file
    with open(TEMP_FiLE, 'w') as temp_file:
        for line in rotated_lines:
            temp_file.write(line + '\n')

with open(TEMP_FiLE, 'r') as file:
    operation = ''
    for line in file:
        if(line.strip() == ''):
            print( (f"Intermediate result: {intermediate_result}"))
            RESULT += intermediate_result
            continue
        if line.startswith('*'):
            operation = '*'
            intermediate_result = 1
        elif line.startswith('+'):
            operation = '+'
            intermediate_result = 0

        values = re.findall(r'(\d)', line)
        # swap the values left to right
        values = values[::-1]
        # convert it to a string (e.g. ['1','2','3'] -> 123)
        value = 0
        for value_str in values:
            value = value * 10 + int(value_str)
        
        if operation == '+':
            intermediate_result += value
        elif operation == '*':
            intermediate_result *= value

    print( (f"Intermediate result: {intermediate_result}"))
    RESULT += intermediate_result
    print (f"result: {RESULT}")
