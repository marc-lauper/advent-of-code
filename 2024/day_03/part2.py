import re;

VERBOSE = False
DEBUG = False

def print_verbose(text):
    if VERBOSE:
        print(text)
        

def print_debug(text):
    if DEBUG:
        print(text)

with open('input.txt', 'r') as file:
    result = 0
    enabled = True
    
    for line in file:
        valids = re.findall(r'(mul\(\d+,\d+\)|don\'t\(\)|do\(\))', line)
        for valid in valids:
            print_verbose(f"valid: {valid}")
            if(valid == "do()"):
                enabled = True
            elif(valid == "don't()"):
                enabled = False
            elif(enabled):
                values = re.findall(r'\d+', valid)
                print_debug(f"values: {values}")
                result += int(values[0]) * int(values[1])
    
    print (f"result: {result}")
