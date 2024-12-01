import re;

VERBOSE = False
DEBUG = True

def print_verbose(text):
    if VERBOSE:
        print(text)
        

def print_debug(text):
    if DEBUG:
        print(text)

with open('input.txt', 'r') as file:
    list_left = []
    dic_right = {}
    
    for line in file:
        location_ids = re.findall(r'(\d+)\s+(\d+)', line)[0]
        print_debug(f"location_ids: {location_ids}")
        list_left.append(int(location_ids[0]))
        right_id = int(location_ids[1])
        dic_right[right_id] = dic_right.get(right_id, 0) + 1

    result = 0
    for i in range(len(list_left)):
        occurrences = dic_right[list_left[i]] if list_left[i] in dic_right else 0
        print_debug(f"list_left[i]: {list_left[i]}, occurrences: {occurrences}")
        result += list_left[i] * occurrences
    
    print (f"result: {result}")
