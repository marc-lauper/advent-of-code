import re;

USE_EXAMPLE = False
FILE = 'example.txt' if USE_EXAMPLE else  'input.txt'

LEN = 12
VERBOSE = FILE != 'input.txt'
DEBUG = False # FILE == 'example.txt'

def print_verbose(text):
    if VERBOSE:
        print(text)
        

def print_debug(text):
    if DEBUG:
        print(text)

def find_biggest(batteries, lowerBound, higherBound):
    biggest = -1
    position = -1
    print_debug(f"find_biggest from {lowerBound} to {higherBound}, e.g. from array {batteries[lowerBound:higherBound]}")
    for i in range(lowerBound, higherBound):
        battery = int(batteries[i])
        if battery > biggest:
            biggest = battery
            position = i
        if battery == 9:
            break
    assert biggest != -1
    return biggest, position

with open(FILE, 'r') as file:
    result = 0
    
    for line in file:
        batteries = re.findall(r'(\d)', line)
        print_verbose(f"batteries: {batteries}")
        joltage_digits = []
        remaining_len = LEN
        position = -1
        while len(joltage_digits) < LEN:
            biggest, position = find_biggest(batteries, position + 1, len(batteries)-remaining_len+1)
            joltage_digits.append(biggest)
            remaining_len -= 1
        
        joltage = 0
        for digit in joltage_digits:
            joltage = joltage * 10 + digit
        print_verbose (f"line: {line.strip()} -> joltage_digits: {joltage_digits}, joltage: {joltage}")
        result += joltage

    print (f"result: {result}")
