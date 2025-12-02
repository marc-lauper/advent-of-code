import re;

LIMIT = 100
USE_EXAMPLE = False
FILE = 'example.txt' if USE_EXAMPLE else  'input.txt'

VERBOSE = True # FILE != 'input.txt'
DEBUG = FILE == 'example.txt'

def print_verbose(text):
    if VERBOSE:
        print(text)
        

def print_debug(text):
    if DEBUG:
        print(text)

def step(position, direction, distance):
        position_before = position
        new_position_before_mod = position + (distance if direction == 'R' else -distance)
        nb_of_times_crossed_zero = 0
        position = new_position_before_mod
        below_zero = position < 0


        while position < 0:
            nb_of_times_crossed_zero += 1
            position += LIMIT
        while position > LIMIT:
            nb_of_times_crossed_zero += 1
            position -= LIMIT

        if position == LIMIT:
            position = 0

        if position == 0:
            nb_of_times_crossed_zero += 1

        if position_before == 0 and below_zero:
            nb_of_times_crossed_zero -= 1

        if direction == 'R':
            print_verbose(f"Moving R by {distance} from {position_before} to {position} ({new_position_before_mod}), crossed zero {nb_of_times_crossed_zero} times")
        else:
            print_verbose(f"Moving L by {distance} from {position_before} to {position} ({new_position_before_mod}), crossed zero {nb_of_times_crossed_zero} times")
        
        return (position, nb_of_times_crossed_zero)

with open(FILE, 'r') as file:

    # First, a series of tests to isolate weird corner cases
    assert step(50, 'R', 30) == (80, 0)
    assert step(50, 'R', 50) == (0, 1)
    assert step(80, 'R', 30) == (10, 1)
    assert step(50, 'R', 150) == (0, 2)
    assert step(80, 'R', 130) == (10, 2)

    assert step(10, 'L', 5) == (5, 0)
    assert step(10, 'L', 10) == (0, 1)
    assert step(10, 'L', 20) == (90, 1)
    assert step(10, 'L', 110) == (0, 2)
    assert step(10, 'L', 120) == (90, 2)

    assert step(0, 'L', 1) == (99, 0)
    assert step(1, 'L', 2) == (99, 1)
    assert step(0, 'L', 101) == (99, 1)
    assert step(1, 'L', 102) == (99, 2)
    assert step(0, 'R', 1) == (1, 0)
    assert step(0, 'R', 101) == (1, 1)
    assert step(99, 'R', 2) == (1, 1)
    assert step(99, 'R', 102) == (1, 2)

    assert step(0, 'L', 100) == (0, 1)
    assert step(0, 'R', 100) == (0, 1)
    assert step(50, 'R', 250) == (0, 3)
    assert step(50, 'L', 250) == (0, 3)

    # The real code starts here
    position = 50
    result = 0
    print_verbose(f"position: {position}")
    
    for line in file:
        values = re.findall(r'([LR])(\d+)', line)[0]
        print_debug(f"values: {values}")
        direction = values[0]
        distance = int(values[1])
        if distance == 0:
            continue

        position, crosses = step(position, direction, distance)
        result += crosses

    print (f"result: {result}")