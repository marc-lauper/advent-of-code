import re

USE_EXAMPLE = False
FILE = 'example.txt' if USE_EXAMPLE else  'input.txt'

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
    
    for line in file:
        values = re.findall(r'(\d+)', line)
        # Does it match?
        if not values:
            OPERATIONS = re.findall(r'([+*])', line)
            print_debug(f"operations: {OPERATIONS}")
        else:
            print_debug(f"values: {values}")
            ROWS.append( [int(v) for v in values] )
    
    # print the rows
    print_debug(f"ROWS: {ROWS}")
    
    row_limit = len(ROWS)
    col_limit = len(ROWS[0])
    for col in range(col_limit):
        operation = OPERATIONS[col]
        if operation == '+':
            col_result = 0
        else:
            col_result = 1

        for row in range(row_limit):
            value = ROWS[row][col]
            print_debug(f"Processing row {row}, col {col}, value {value} with operation {operation}")
            if operation == '+':
                col_result += value
            elif operation == '*':
                col_result *= value
        print_debug(f"col_result[{col}] is {col_result}")
        RESULT += col_result
    
    print (f"result: {RESULT}")
