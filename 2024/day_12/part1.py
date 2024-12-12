import re;

VERBOSE = True
DEBUG = False
row_limit = 0
column_limit = 0
index = 0
input_array = []
indexed_array = []
area_by_index = {}
border_by_index = {}
symbol_by_index = {}
current_start = (0, 0)

def print_verbose(text):
    if VERBOSE:
        print(text)

def print_debug(text):
    if DEBUG:
        print(text)

def find_next_start():
    global indexed_array
    global current_start
    global row_limit
    global column_limit
    
    for row in range(row_limit):
        for column in range(column_limit):
            if indexed_array[row][column] is None:
                current_start = (row, column)
                return
    current_start = None

def get_neighbors(row, column):
    global input_array
    global row_limit
    global column_limit
    neighbors = []

    if row > 0:
        neighbors.append((row - 1, column, input_array[row - 1][column]))
    if row < row_limit - 1:
        neighbors.append((row + 1, column, input_array[row + 1][column]))
    if column > 0:
        neighbors.append((row, column - 1, input_array[row][column - 1]))
    if column < column_limit - 1:
        neighbors.append((row, column + 1, input_array[row][column + 1]))
    return neighbors

def build_indexed_array(row = 0, column = 0):
    global input_array
    global indexed_array
    global row_limit
    global column_limit
    global index

    indexed_array[row][column] = index
    area_by_index[index] = area_by_index.get(index, 0) + 1
    symbol_by_index[index] = input_array[row][column]
    neighbors = get_neighbors(row, column)
    # Retrieve the neighbors with the same plant
    similar_neighbors = [neighbor for neighbor in neighbors if neighbor[2] == input_array[row][column]]

    # Retrieve the neighbors with a different plant
    different_neighbors = [neighbor for neighbor in neighbors if neighbor[2] != input_array[row][column]]
    border_by_index[index] = border_by_index.get(index, 0) + len(different_neighbors) + (4 - len(neighbors))
    
    print_debug(f"[{input_array[row][column]}[{row}][{column}]] similar_neighbors: {similar_neighbors}")
    print_debug(f"[{input_array[row][column]}[{row}][{column}]] different_neighbors: {different_neighbors}")

    for neighbor in similar_neighbors:
        if indexed_array[neighbor[0]][neighbor[1]] is None:
            build_indexed_array(neighbor[0], neighbor[1])

with open('input.txt', 'r') as file:
    result = 0

    for line in file:
        input_array.append(list(line.strip()))
        column_limit = len(input_array[-1])
        indexed_array.append([None] * column_limit)
        row_limit += 1

    done = False
    while not done:
        find_next_start()
        if current_start is None:
            done = True
        else:
            build_indexed_array(current_start[0], current_start[1])
            index += 1

    print_verbose(f"Found {index-1} areas")
    print_verbose(f"Symbol by index: {symbol_by_index}")
    for i in range(index):
        print_verbose(f"index: {i} symbol: {symbol_by_index[i]} area: {area_by_index[i]} border: {border_by_index[i]}")
        result += area_by_index[i] * border_by_index[i]

    print (f"\nresult: {result}")
