import re;

VERBOSE = True
DEBUG = True
robots = []
x_limit = 101
y_limit = 103
steps = 100

def print_verbose(text):
    if VERBOSE:
        print(text)

def print_debug(text):
    if DEBUG:
        print(text)

def print_grid():
    if not DEBUG:
        return
    for y in range(y_limit):
        for x in range(x_limit):
            # Number of robots in this position
            nb_of_bots = len([robot for robot in robots if robot[0] == (x, y)])
            if nb_of_bots > 0:
                print(nb_of_bots, end="")
            else:
                print(".", end="")
        print()

def move_robot(robot, iterations):
    position = robot[0]
    velocity = robot[1]
    new_position = (position[0] + velocity[0] * iterations, position[1] + velocity[1] * iterations)
    new_position = (new_position[0] % x_limit, new_position[1] % y_limit)
    return new_position

def count_by_quadrants(robots):
    x_middle = x_limit // 2
    y_middle = y_limit // 2
    
    q1 = len([robot for robot in robots if robot[0][0] < x_middle and robot[0][1] < y_middle])
    q2 = len([robot for robot in robots if robot[0][0] > x_middle and robot[0][1] < y_middle])
    q3 = len([robot for robot in robots if robot[0][0] < x_middle and robot[0][1] > y_middle])
    q4 = len([robot for robot in robots if robot[0][0] > x_middle and robot[0][1] > y_middle])
    
    print_debug(f"q1: {q1}, q2: {q2}, q3: {q3}, q4: {q4}")
    return q1*q2*q3*q4

with open('input.txt', 'r') as file:
    result = 0

    i = 0
    x_values = [None, None, None]
    y_values = [None, None, None]
    for line in file:
        numbers = re.findall(r'=([\d-]+),([\d-]+)', line)
        if len(numbers) == 0:
            continue
        position = (int(numbers[0][0]), int(numbers[0][1]))
        velocity = (int(numbers[1][0]), int(numbers[1][1]))
        robots.append((position, velocity))
        print_debug(f"position: {position}, velocity: {velocity}")  
    
    # print_debug(f"robots: {robots}")
    # print_grid()
    
    for i in range(len(robots)):
        robots[i] = (move_robot(robots[i], steps), robots[i][1])
    
    print_debug(f"After moving {steps} times:")
    print_grid()

    result = count_by_quadrants(robots)
    print (f"\nresult: {result}")
