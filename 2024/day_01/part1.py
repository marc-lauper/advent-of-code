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
    list_left = []
    list_right = []
    
    for line in file:
        location_ids = re.findall(r'(\d+)\s+(\d+)', line)[0]
        print_debug(f"location_ids: {location_ids}")
        list_left.append(int(location_ids[0]))
        list_right.append(int(location_ids[1]))
        print_debug(f"left: {list_left}, right: {list_right}")
        
    list_left.sort()
    list_right.sort()
    print_debug(f"left: {list_left}, right: {list_right}")
    
    result = 0
    for i in range(len(list_left)):
        diff = abs(list_left[i] - list_right[i])
        result += diff
    
    print (f"result: {result}")
