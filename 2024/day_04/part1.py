import re;

VERBOSE = False
DEBUG = False
SEARCHED = ['X', 'M', 'A', 'S']

def print_verbose(text):
    if VERBOSE:
        print(text)
        

def print_debug(text):
    if DEBUG:
        print(text)

# Direction is 1 to 8:
# 123
# 4.5
# 678
# (e.g. 1 is up-left, 2 is up, 3 is up-right, 4 is left, 5 is right, 6 is down-left, 7 is down, 8 is down-right)
def find_xmas(array, pos_x, pos_y, direction = 0, current_xmas_index = 0):
    if current_xmas_index == len(SEARCHED):
        print_debug(f"Found XMAS ending at {pos_x}, {pos_y}")
        return 1
    if(pos_x < 0 or pos_x >= len(array) or pos_y < 0 or pos_y >= len(array[0])):
        return 0
    if array[pos_x][pos_y] != SEARCHED[current_xmas_index]:
        return 0
    if(direction != 0):
        print_debug(f"Found {SEARCHED[current_xmas_index]}")
    if direction == 1:
        return find_xmas(array, pos_x - 1, pos_y - 1, direction, current_xmas_index + 1)
    if direction == 2:
        return find_xmas(array, pos_x - 1, pos_y, direction, current_xmas_index + 1)
    if direction == 3:
        return find_xmas(array, pos_x - 1, pos_y + 1, direction, current_xmas_index + 1)
    if direction == 4:
        return find_xmas(array, pos_x, pos_y - 1, direction, current_xmas_index + 1)
    if direction == 5:
        return find_xmas(array, pos_x, pos_y + 1, direction, current_xmas_index + 1)
    if direction == 6:
        return find_xmas(array, pos_x + 1, pos_y - 1, direction, current_xmas_index + 1)
    if direction == 7:
        return find_xmas(array, pos_x + 1, pos_y, direction, current_xmas_index + 1)
    if direction == 8:
        return find_xmas(array, pos_x + 1, pos_y + 1, direction, current_xmas_index + 1)
    if(direction == 0):
        result = 0
        for direction in range(1, 9):
            result += find_xmas(array, pos_x, pos_y, direction, current_xmas_index)
        return result
    return 0

with open('input.txt', 'r') as file:
    result = 0
    
    # Build a two-dimension array based on the content of the file
    array = []
    for line in file:
        array.append(list(line.strip()))

    # print_debug(f"array: {array}")
    for i in range(len(array)):
        for j in range(len(array[i])):
            if array[i][j] == 'X':
                result += find_xmas(array, i, j)
    print (f"result: {result}")
