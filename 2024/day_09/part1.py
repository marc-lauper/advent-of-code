import re;
from functools import cmp_to_key;

VERBOSE = True
DEBUG = True

def print_verbose(text):
    if VERBOSE:
        print(text)

def print_debug(text):
    if DEBUG:
        print(text)

def compact(ids):
    result = 0
    i = 0
    j = len(ids) - 1
    current_position = 0
    right_data = ids[j]

    # Make sure the right data points to valid data
    if right_data[0] is None:
        print_debug(f"right_data[0] is None")
        j -= 1
        right_data = ids[j]
        print_debug(f"right_data[0] is now {right_data[0]}")

    while i<= j:
        left_data = ids[i]
        right_data = ids[j]

        if left_data[0] is not None:
            length = left_data[1]
            for _ in range(0, length):
                result += current_position * left_data[0]
                print(f"{left_data[0]}", end="")
                current_position += 1
            i += 1

        else:
            length = min(left_data[1], right_data[1])
            for _ in range(0, length):
                result += current_position * right_data[0]
                print(f"{right_data[0]}", end="")
                current_position += 1
            # print_debug (f"right_data[1] = {right_data[1]}")
            right_data = (right_data[0], right_data[1] - length)
            if right_data[1] == 0:
                j -= 2
            else:
                ids[j] = right_data
            
            left_data = (left_data[0], left_data[1] - length)
            if left_data[1] == 0:
                i += 1
            else:
                ids[i] = left_data
    
    return result
        
            
        

with open('input.txt', 'r') as file:
    result = 0

    ids = []
    current_id = 0
    is_data = True
    for line in file:
        for char in line:
            if is_data:
                ids.append((current_id, int(char)))
                current_id += 1
                is_data = False
            else:
                ids.append((None, int(char)))
                is_data = True
    
    if DEBUG:
        for data, length in ids:
            for i in range(0, length):
                if data is not None:
                    print(f"{data}", end="")
                else:
                    print(".", end="")
        print()
    
    result = compact(ids)
    print (f"\nresult: {result}")
