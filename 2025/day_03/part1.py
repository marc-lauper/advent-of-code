import re;

USE_EXAMPLE = False
FILE = 'example.txt' if USE_EXAMPLE else  'input.txt'

VERBOSE = FILE != 'input.txt'
DEBUG = FILE == 'example.txt'

def print_verbose(text):
    if VERBOSE:
        print(text)
        

def print_debug(text):
    if DEBUG:
        print(text)

def find_biggest(batteries, lowerBound, higherBound):
    biggest = -1
    position = -1
    for i in range(lowerBound, higherBound):
        battery = int(batteries[i])
        if battery > biggest:
            biggest = battery
            position = i
        if battery == 9:
            break
    return biggest, position

with open(FILE, 'r') as file:
    result = 0
    
    for line in file:
        batteries = re.findall(r'(\d)', line)
        print_verbose(f"batteries: {batteries}")

        biggest, position = find_biggest(batteries, 0, len(batteries)-1)
        biggest_after, position = find_biggest(batteries, position + 1, len(batteries))
        joltage = biggest * 10 + biggest_after
        print_verbose (f"line: {line.strip()} -> biggest: {biggest}, biggest after: {biggest_after}, joltage: {joltage}")
        result += joltage

    print (f"result: {result}")
