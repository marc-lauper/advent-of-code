import re

USE_EXAMPLE = False
FILE = 'example.txt' if USE_EXAMPLE else  'input.txt'

VERBOSE = FILE != 'input.txt'
DEBUG = FILE == 'example.txt'
RESULT = 0
FRESH_INGREDIENTS_RANGES = []

def print_verbose(text):
    if VERBOSE:
        print(text)
        

def print_debug(text):
    if DEBUG:
        print(text)

with open(FILE, 'r') as file:
    
    parsing_ranges = True
    for line in file:
        if parsing_ranges:
            line = line.strip()
            if line == "":
                parsing_ranges = False
                continue
            parts = line.split("-")
            FRESH_INGREDIENTS_RANGES.append( (int(parts[0]), int(parts[1])) )
    
    print_debug(f"FRESH_INGREDIENTS_RANGES: {FRESH_INGREDIENTS_RANGES}")
    
    FRESH_INGREDIENTS_RANGES.sort()
    consolidated_ranges = []
    current_start, current_end = FRESH_INGREDIENTS_RANGES[0]
    for start, end in FRESH_INGREDIENTS_RANGES[1:]:
        if start <= current_end + 1:
            current_end = max(current_end, end)
        else:
            consolidated_ranges.append((current_start, current_end))
            current_start, current_end = start, end
    consolidated_ranges.append((current_start, current_end))

    for start, end in consolidated_ranges:
        RESULT += (end - start + 1)
    
    print (f"result: {RESULT}")
