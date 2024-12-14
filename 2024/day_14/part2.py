import re;
from PIL import Image, ImageDraw, ImageFont;

VERBOSE = True
DEBUG = True
robots = []
x_limit = 101
y_limit = 103

def print_verbose(text):
    if VERBOSE:
        print(text)

def print_debug(text):
    if DEBUG:
        print(text)

def print_grid(name):
    im = Image.new( 'RGB', (x_limit,y_limit), "white") # Create a new black image
    pixels = im.load() # Create the pixel map

    for y in range(y_limit):
        for x in range(x_limit):
            # Number of robots in this position
            nb_of_bots = len([robot for robot in robots if robot[0] == (x, y)])
            if nb_of_bots > 0:
                pixels[x, y] = (0, 0, 0) 

    # Save Image
    im.save(f"output/{name}.png", "PNG")

def move_robot(robot, iterations):
    position = robot[0]
    velocity = robot[1]
    new_position = (position[0] + velocity[0] * iterations, position[1] + velocity[1] * iterations)
    new_position = (new_position[0] % x_limit, new_position[1] % y_limit)
    return new_position

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
    
    # The boundaries (between 7000 and 8000) have been defined by trying random values in the answer box. Sorry, not sorry.
    initial_step = 7000
    for i in range(len(robots)):
            robots[i] = (move_robot(robots[i], 7000), robots[i][1])

    for inc in range(1000):
        step = initial_step + inc + 1
        print(f"Step: {step}", end="\r")
        for i in range(len(robots)):
            robots[i] = (move_robot(robots[i], 1), robots[i][1])
        print_grid(str(step))