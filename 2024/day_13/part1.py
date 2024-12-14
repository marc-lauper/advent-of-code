import re;

VERBOSE = True
DEBUG = True
arcades = []

def print_verbose(text):
    if VERBOSE:
        print(text)

def print_debug(text):
    if DEBUG:
        print(text)

def resolve_arcade(arcade):
    x_values = arcade[0]
    y_values = arcade[1]
    print_debug(f"x_values: {x_values}")
    print_debug(f"y_values: {y_values}")
    determinant = x_values[0] * y_values[1] - y_values[0] * x_values[1]
    
    if determinant == 0:
        return None, None
    
    # Calculate A and B using Cramer's rule
    a = (x_values[2] * y_values[1] - y_values[2] * x_values[1]) / determinant
    b = (x_values[0] * y_values[2] - y_values[0] * x_values[2]) / determinant

    # Check if it's possible to end up at the exact desired location
    if a.is_integer() and b.is_integer():
        print_debug(f"a: {a}")
        print_debug(f"b: {b}")
        cost = 3*int(a) + int(b)
        print_debug(f"cost: {cost}")
        return cost
    else:
        print_debug("Impossible to solve")
        return 0

with open('input.txt', 'r') as file:
    result = 0

    i = 0
    x_values = [None, None, None]
    y_values = [None, None, None]
    for line in file:
        numbers = re.findall(r'(\d+)', line)
        if len(numbers) == 0:
            continue
        print_debug(f"numbers: {numbers}")
        index = i%3
        x_values[index] = int(numbers[0])
        y_values[index] = int(numbers[1])
        i += 1
        if(index == 2):
            arcades.append([x_values, y_values])
            x_values = [None, None, None]
            y_values = [None, None, None]
    
    for arcade in arcades:
        result += resolve_arcade(arcade)

    print (f"\nresult: {result}")
