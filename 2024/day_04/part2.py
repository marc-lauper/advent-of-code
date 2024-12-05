import re;

VERBOSE = True
DEBUG = False

def print_verbose(text):
    if VERBOSE:
        print(text)
        

def print_debug(text):
    if DEBUG:
        print(text)

def find_mas(array, pos_x, pos_y):
    top_left= [pos_x-1, pos_y-1]
    top_right = [pos_x-1, pos_y+1]
    bottom_left = [pos_x+1, pos_y-1]
    bottom_right = [pos_x+1, pos_y+1]

    if top_left[0] < 0 or top_left[1] < 0:
        return 0
    if top_right[0] < 0 or top_right[1] >= len(array[0]):
        return 0
    if bottom_left[0] >= len(array) or bottom_left[1] < 0:
        return 0
    if bottom_right[0] >= len(array) or bottom_right[1] >= len(array[0]):
        return 0
    
    diag_1 = array[top_left[0]][top_left[1]] + array[pos_x][pos_y] + array[bottom_right[0]][bottom_right[1]]
    diag_2 = array[top_right[0]][top_right[1]] + array[pos_x][pos_y] + array[bottom_left[0]][bottom_left[1]]
    
    print_verbose(f"diag_1: {diag_1}, diag_2: {diag_2}")
    
    if((diag_1 == 'MAS' or diag_1 == 'SAM') and (diag_2 == 'MAS' or diag_2 == 'SAM')):
        return 1
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
            if array[i][j] == 'A':
                result += find_mas(array, i, j)
    print (f"result: {result}")
