import re;
from functools import cmp_to_key;

VERBOSE = False
DEBUG = False
POSSIBLE_OPERATORS = ['+', '*']

def print_verbose(text):
    if VERBOSE:
        print(text)

def print_debug(text):
    if DEBUG:
        print(text)
        
def is_possible(expected, numbers, current_val = 0, next_operator = '+'):
    if len(numbers) == 0:
        return current_val == expected

    current_val = eval(f"{current_val} {next_operator} {numbers[0]}")
    print_debug(f"current_val: {current_val}")
    if current_val > expected:
        return False

    numbers = numbers[1:]
    for next_operator in POSSIBLE_OPERATORS:
        if is_possible(expected, numbers, current_val, next_operator):
            return True

    return False
    

with open('input.txt', 'r') as file:
    result = 0

    for line in file:
        if(len(line) < 2):
            continue
        numbers = re.findall(r'\d+', line)
        if numbers:
            expected = int(numbers[0])
            numbers = list(map(int, numbers[1:]))
            print_debug(f"expected: {expected}, numbers: {numbers}")
            if(is_possible(expected, numbers)):
                result += int(expected)
    
    print (f"result: {result}")
