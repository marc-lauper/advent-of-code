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

def print_ids(ids):
    if DEBUG:
        for data, length, position in ids:
            for _ in range(0, length):
                if data is not None:
                    print(f"{data}", end="")
                else:
                    print(".", end="")
        print()

def compute_result(ids):
    result = 0

    for data, length, position in ids:

        if data is not None:
            for _ in range(0, length):
                result += position * data
                print(f"{data}", end="")
                position += 1
    
    return result

def compact(ids):
    # result = 0
    # i = 0
    j = len(ids) - 1
    right_data = ids[j]

    # Make sure the right data points to valid data
    if right_data[0] is None:
        print_debug(f"right_data[0] is None")
        j -= 1
        right_data = ids[j]
        print_debug(f"right_data[0] is now {right_data[0]}")

    while j > 0:
        moved = False
        right_data = ids[j]
        if(right_data[0] is None):
            j -= 1
            continue
        print_debug(f"trying to move: {right_data}")
        i = 0

        while i < j and not moved:
            left_data = ids[i]
            if left_data[0] is None:
                if right_data[1] <= left_data[1]:
                    diff = left_data[1] - right_data[1]
                    ids[i] = (right_data[0], right_data[1], left_data[2])
                    ids[j] = (None, right_data[1], right_data[2])
                    if diff > 0:
                        # Insert a new record right after ids[i]
                        ids.insert(i+1, (None, diff, left_data[2] + right_data[1]))
                        j += 1
                    moved = True
                    print_verbose(f"Moved {right_data} to {left_data}")
                else:
                    print_verbose(f"Cannot move {right_data} to {left_data}")
            i += 1

        # File it too big to fit, try the next one
        j -= 1
        print_ids(ids)
    
    return ids
        
            
        

with open('input.txt', 'r') as file:
    result = 0

    ids = []
    current_id = 0
    position = 0
    is_data = True
    for line in file:
        for char in line:
            if is_data:
                ids.append((current_id, int(char), position))
                current_id += 1
                is_data = False
            else:
                ids.append((None, int(char), position))
                is_data = True
            position += int(char)
    
    print_ids(ids)
    ids = compact(ids)
    result = compute_result(ids)
    print (f"\nresult: {result}")
