import re;
from functools import cmp_to_key;

VERBOSE = False
DEBUG = False

def print_verbose(text):
    if VERBOSE:
        print(text)

def print_debug(text):
    if DEBUG:
        print(text)

def blink(stones):
    result = []
    for stone in stones:
        stoneAsStr = str(stone)
        if stone == 0:
            result.append(1)
        elif len(stoneAsStr) % 2 == 0:
            left_half = stoneAsStr[:len(stoneAsStr)//2]
            right_half = stoneAsStr[len(stoneAsStr)//2:]
            result.append(int(left_half))
            result.append(int(right_half))
        else:
            result.append(stone * 2024)
    return result
            

with open('input.txt', 'r') as file:
    result = 0
    starting_row = 0

    # Build a two-dimension array based on the content of the file
    for line in file:
        stones = re.findall(r'\d+', line)
        stones = list(map(int, stones))

    print_debug(f"stones: {stones}")
    
    # Execute blink 25 times
    for i in range(75):
        stones = blink(stones)
        print_debug(f"stones: {stones}")

    print (f"\nresult: {len(stones)}")
