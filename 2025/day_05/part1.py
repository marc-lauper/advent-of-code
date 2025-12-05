import re

USE_EXAMPLE = False
FILE = 'example.txt' if USE_EXAMPLE else  'input.txt'

VERBOSE = FILE != 'input.txt'
DEBUG = FILE == 'example.txt'
RESULT = 0
FRESH_INGREDIENTS_RANGES = []
AVAILABLE_INGREDIENT_IDS = []

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
        else:
            AVAILABLE_INGREDIENT_IDS.append( int(line))
    
    print_debug(f"FRESH_INGREDIENTS_RANGES: {FRESH_INGREDIENTS_RANGES}")
    print_debug(f"AVAILABLE_INGREDIENT_IDS: {AVAILABLE_INGREDIENT_IDS}")
    
    for ingredient_id in AVAILABLE_INGREDIENT_IDS:
        is_fresh = False
        for fr in FRESH_INGREDIENTS_RANGES:
            if fr[0] <= ingredient_id <= fr[1]:
                is_fresh = True
                break
        if is_fresh:
            RESULT += 1
            print_debug(f"Ingredient ID {ingredient_id} is fresh.")
        else:
            print_debug(f"Ingredient ID {ingredient_id} is NOT fresh.")
    
    print (f"result: {RESULT}")
