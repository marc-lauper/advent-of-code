VERBOSE = False
DEBUG = False
row_limit = 0
col_limit = 0

def print_verbose(text):
    if VERBOSE:
        print(text)

def print_debug(text):
    if DEBUG:
        print(text)

def find_antinodes(first_antenna, second_antenna):
    result = set()
    # The paired antennas are all exactly in line with two antennas, so they are all also antinodes
    result.add(first_antenna)
    result.add(second_antenna)

    x1 = first_antenna[0]
    y1 = first_antenna[1]
    x2 = second_antenna[0]
    y2 = second_antenna[1]

    x_distance = x1 - x2
    y_distance = y1 - y2
    
    x3 = x1
    y3 = y1
    can_add = True
    while can_add:
        x3 = x3 + x_distance
        y3 = y3 + y_distance
        if x3 >= 0 and x3 < row_limit and y3 >= 0 and y3 < col_limit:
            result.add((x3, y3))
            # print_verbose(f"x3: {x3}, y3: {y3}")
        else:
            can_add = False
        
    x4 = x2
    y4 = y2
    can_add = True
    while can_add:
        x4 = x4 - x_distance
        y4 = y4 - y_distance
        if x4 >= 0 and x4 < row_limit and y4 >= 0 and y4 < col_limit:
            result.add((x4, y4))
            # print_verbose(f"x4: {x4}, y4: {y4}")
        else:
            can_add = False
    
    return result

def find_antinodes_for_list(antenna_list):
    antinodes = set()
    for i in range(0, len(antenna_list)):
        for j in range(i + 1, len(antenna_list)):
            new_antinodes = find_antinodes(antenna_list[i], antenna_list[j])
            antinodes.update(new_antinodes)
            new_antinodes = find_antinodes(antenna_list[j], antenna_list[i])
            antinodes.update(new_antinodes)
    return antinodes

with open('input.txt', 'r') as file:
    result = 0

    row = 0
    antennas = {}
    for line in file:
        for column in range(0, len(line)):
            if(line[column] != '.' and line[column] != '\n'):
                symbol = line[column]
                # antennas is a dictionnary. The key is "symbol", the value is a list of all the columns where it was found
                if symbol in antennas:
                    antennas[symbol].append((row, column))
                else:
                    antennas[symbol] = [(row, column)]
        row += 1
        row_limit += 1
        col_limit = len(line) -1 # Because of \n
    
    print_debug(f"antennas: {antennas}")
    print_debug(f"row_limit: {row_limit}")
    print_debug(f"col_limit: {col_limit}")
    
    antinodes = set()
    for key in antennas:
        print_verbose(f"key: {key}")
        print_verbose(f"antennas[key]: {antennas[key]}")
        new_antinodes = find_antinodes_for_list(antennas[key])
        antinodes.update(new_antinodes)
    
    antinodes_count = len(antinodes)
    print_verbose(f"antinodes: {antinodes}")
    if VERBOSE:
        for row in range(0, row_limit):
            for col in range(0, col_limit):
                found_antenna = False
                for key in antennas:
                    if (row, col) in antennas[key]:
                        print(key, end="")
                        found_antenna = True
                        break
                if not found_antenna:
                    if (row, col) in antinodes:
                        print("#", end="")
                    else:
                        print(".", end="")
            print()
    
    print (f"result: {antinodes_count}")
