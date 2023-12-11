# Day 10 - Pipe Maze
See https://adventofcode.com/2023/day/10

## Part 1
```python

import math, sys

sys.setrecursionlimit(10**6)

START = 'S'
NORTH_SOUTH = '|'
EAST_WEST = '-'
NORTH_EAST = 'L'
NORTH_WEST = 'J'
SOUTH_WEST = '7'
SOUTH_EAST = 'F'

NORTH = 0
SOUTH  = 1
EAST = 2
WEST = 3

maze = []
distances = []
with open('aoc10.txt', 'r') as file:
    for line in file:
        row = []
        distances_row = []
        for char in line:
            row.append(char)
            distances_row.append(-1)
        maze.append(row)
        distances.append(distances_row)

def find_start():
    for y in range(0, len(maze)):
        for x in range(0, len(maze[y])):
            if(maze[y][x] == START):
                return x, y
     
def find_next(x, y, direction):
    if(direction == NORTH and y > 0 and (maze[y-1][x] == NORTH_SOUTH or maze[y-1][x] == SOUTH_EAST or maze[y-1][x] == SOUTH_WEST or maze[y-1][x] == START)):
            return x, y-1
    if(direction == SOUTH and y < len(maze) - 1 and (maze[y+1][x] == NORTH_SOUTH or maze[y+1][x] == NORTH_EAST or maze[y+1][x] == NORTH_WEST or maze[y+1][x] == START)):
            return x, y+1
    if(direction == WEST and x > 0 and (maze[y][x-1] == EAST_WEST or maze[y][x-1] == NORTH_EAST or maze[y][x-1] == SOUTH_EAST or maze[y][x-1] == START)):
            return x-1, y
    if(direction == EAST and x < len(maze[y]) - 1 and (maze[y][x+1] == EAST_WEST or maze[y][x+1] == NORTH_WEST or maze[y][x+1] == SOUTH_WEST or maze[y][x+1] == START)):
            return x+1, y
    return None, None

def invert(direction):
    if(direction == NORTH):
        return SOUTH
    if(direction == SOUTH):
        return NORTH
    if(direction == WEST):
        return EAST
    if(direction == EAST):
        return WEST
    return None

def walk_path(x, y, coming_from, distance):
    
    if(x < 0 or x >= len(maze[y]) or y < 0 or y >= len(maze)):
        return None
    
    pipe_type = maze[y][x]
    distances[y][x] = distance

    if(pipe_type == NORTH_SOUTH):
        direction = SOUTH if coming_from == NORTH else NORTH
    elif(pipe_type == EAST_WEST):
        direction = WEST if coming_from == EAST else EAST
    elif(pipe_type == NORTH_EAST):
        direction = EAST if coming_from == NORTH else NORTH
    elif(pipe_type == NORTH_WEST):
        direction = WEST if coming_from == NORTH else NORTH
    elif(pipe_type == SOUTH_EAST):
        direction = EAST if coming_from == SOUTH else SOUTH
    elif(pipe_type == SOUTH_WEST):
        direction = WEST if coming_from == SOUTH else SOUTH
    else:
         return None
    
    next_x, next_y = find_next(x, y, direction)
    if(next_x == None):
        return None

    print (pipe_type + " -> " + maze[next_y][next_x] + " (" + str(x) + ", " + str(y) + " to " + str(next_x) + ", " + str(next_y) + ")")
    
    if(distances[next_y][next_x] == 0):
        return math.ceil(distance/2)
    
    distance = distance + 1
    return walk_path(next_x, next_y, invert(direction), distance)


start_x, start_y = find_start()
print("start: " + str(start_x) + ", " + str(start_y))
distances[start_y][start_x] = 0

next_x, next_y = find_next(start_x, start_y, EAST)
if(next_x != None):
    print ("S -> " + maze[start_y][start_x+1] + " (" + str(start_x) + ", " + str(start_y) + " to " + str(start_x+1) + ", " + str(start_y) + ")")
    result = walk_path(start_x+1, start_y, WEST, 1)
    if(result != None):
        print("result: " + str(result))
        exit()

next_x, next_y = find_next(start_x, start_y, WEST)
if(next_x != None):
    result = walk_path(start_x-1, start_y, EAST, 1)
    if(result != None):
        print("result: " + str(result))
        exit()

next_x, next_y = find_next(start_x, start_y, NORTH)
if(next_x != None):
    result = walk_path(start_x, start_y-1, SOUTH, 1)
    if(result != None):
        print("result: " + str(result))
        exit()

next_x, next_y = find_next(start_x, start_y, SOUTH)
if(next_x != None):
    result = walk_path(start_x, start_y-1, NORTH, 1)
    if(result != None):
        print("result: " + str(result))
        exit()
```

## Part 2
```python

import math, sys, re

sys.setrecursionlimit(10**6)

START = 'S'
NORTH_SOUTH = '|'
EAST_WEST = '-'
NORTH_EAST = 'L'
NORTH_WEST = 'J'
SOUTH_WEST = '7'
SOUTH_EAST = 'F'

NORTH = 0
SOUTH  = 1
EAST = 2
WEST = 3

maze = []
path = []
distances = []
values = []
with open('aoc10.txt', 'r') as file:
    for line in file:
        row = []
        distances_row = []
        for char in line:
            row.append(char)
            distances_row.append(-1)
        maze.append(row)
        distances.append(distances_row)

def Reset():
    values.clear()
    for y in range(0, len(maze)):
        row = []
        row2 = []
        for x in range(0, len(maze[y])):
            row.append(0)
            row2.append(' ')
        values.append(row)
        path.append(row2)
    
def ComputeArea():
    sum = 0
    for y in range(0, len(path)):
        inside = False
        next_row = path[y]
        next_row = re.sub(r'L-*7', '|', ''.join(next_row))
        next_row = re.sub(r'F-*J', '|', ''.join(next_row))
        next_row = re.sub(r'F-*7', '||', ''.join(next_row))
        next_row = re.sub(r'L-*J', '||', ''.join(next_row))
        next_row = re.sub(r'S', '*', ''.join(next_row)) # This depends of the actual start postion, and was a leap of faith. If i doesn't work, properly replace "S" by its intended tile shape...

        row_sum = 0
        for x in range(0, len(next_row)):
            if(next_row[x] == NORTH_SOUTH):
                inside = not inside
            elif(inside):
              row_sum += 1
        sum += row_sum

    return sum

def find_start():
    for y in range(0, len(maze)):
        for x in range(0, len(maze[y])):
            if(maze[y][x] == START):
                return x, y
     
def find_next(x, y, direction):
    if(direction == NORTH and y > 0 and (maze[y-1][x] == NORTH_SOUTH or maze[y-1][x] == SOUTH_EAST or maze[y-1][x] == SOUTH_WEST or maze[y-1][x] == START)):
            return x, y-1
    if(direction == SOUTH and y < len(maze) - 1 and (maze[y+1][x] == NORTH_SOUTH or maze[y+1][x] == NORTH_EAST or maze[y+1][x] == NORTH_WEST or maze[y+1][x] == START)):
            return x, y+1
    if(direction == WEST and x > 0 and (maze[y][x-1] == EAST_WEST or maze[y][x-1] == NORTH_EAST or maze[y][x-1] == SOUTH_EAST or maze[y][x-1] == START)):
            return x-1, y
    if(direction == EAST and x < len(maze[y]) - 1 and (maze[y][x+1] == EAST_WEST or maze[y][x+1] == NORTH_WEST or maze[y][x+1] == SOUTH_WEST or maze[y][x+1] == START)):
            return x+1, y
    return None, None

def invert(direction):
    if(direction == NORTH):
        return SOUTH
    if(direction == SOUTH):
        return NORTH
    if(direction == WEST):
        return EAST
    if(direction == EAST):
        return WEST
    return None

def walk_path(x, y, coming_from, distance):
    
    if(x < 0 or x >= len(maze[y]) or y < 0 or y >= len(maze)):
        return None
    
    pipe_type = maze[y][x]
    distances[y][x] = distance
    path[y][x] = maze[y][x]

    if(pipe_type == NORTH_SOUTH):
        direction = SOUTH if coming_from == NORTH else NORTH
    elif(pipe_type == EAST_WEST):
        direction = WEST if coming_from == EAST else EAST
    elif(pipe_type == NORTH_EAST):
        direction = EAST if coming_from == NORTH else NORTH
    elif(pipe_type == NORTH_WEST):
        direction = WEST if coming_from == NORTH else NORTH
    elif(pipe_type == SOUTH_EAST):
        direction = EAST if coming_from == SOUTH else SOUTH
    elif(pipe_type == SOUTH_WEST):
        direction = WEST if coming_from == SOUTH else SOUTH
    else:
         return None
    
    next_x, next_y = find_next(x, y, direction)
    if(next_x == None):
        return None

    if(distances[next_y][next_x] == 0):
        path[next_y][next_x] = 'S'
        return math.ceil(distance/2)
    
    distance = distance + 1
    return walk_path(next_x, next_y, invert(direction), distance)


start_x, start_y = find_start()
print("start: " + str(start_x) + ", " + str(start_y))
distances[start_y][start_x] = 0

Reset()
next_x, next_y = find_next(start_x, start_y, EAST)
if(next_x != None):
    print ("S -> " + maze[start_y][start_x+1] + " (" + str(start_x) + ", " + str(start_y) + " to " + str(start_x+1) + ", " + str(start_y) + ")")
    result = walk_path(start_x+1, start_y, WEST, 1)
    if(result != None):
        print("result1: " + str(result))
        print("result2: " + str(ComputeArea()))
        exit()

Reset()
next_x, next_y = find_next(start_x, start_y, WEST)
if(next_x != None):
    result = walk_path(start_x-1, start_y, EAST, 1)
    if(result != None):
        print("result1: " + str(result))
        print("result2: " + str(ComputeArea()))
        exit()

Reset()
next_x, next_y = find_next(start_x, start_y, NORTH)
if(next_x != None):
    result = walk_path(start_x, start_y-1, SOUTH, 1)
    if(result != None):
        print("result1: " + str(result))
        print("result2: " + str(ComputeArea()))
        exit()

Reset()
next_x, next_y = find_next(start_x, start_y, SOUTH)
if(next_x != None):
    result = walk_path(start_x, start_y-1, NORTH, 1)
    if(result != None):
        print("result1: " + str(result))
        print("result2: " + str(ComputeArea()))
        exit()
```