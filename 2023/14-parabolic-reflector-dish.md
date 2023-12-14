# Day 14 - Parabolic Reflector Dish
See https://adventofcode.com/2023/day/14

## Part 1
```python
VERBOSE = False
DEBUG = False

def print_verbose(text):
    if VERBOSE:
        print(text)
        

def print_debug(text):
    if DEBUG:
        print(text)

def print_puzzle(lines):
    for line in lines:
        print_verbose(f"   {line}")

def rotate_clockwise(lines):
    return list(zip(*lines[::-1]))

def solve(lines):
    result = 0
    for line in lines:
        print_debug(f"Processing line: {line}")
        current_value = len(line)
        for i in range(len(line)-1, -1, -1):
            char = line[i]
            print_debug(f"  [{i}] char: {char}, current_value: {current_value}")
            if(char == '#'):
                current_value = i
            elif(char == 'O'):
                result += current_value
                current_value -= 1
            print(f"  result: {result}")

    return result

lines = []
with open('aoc14.txt', 'r') as file:
    for line in file:
        line = line.replace('\n', '')
        if(len(line) == 0):
            continue
        lines.append(line)

    print_verbose("Puzzle before rotation:")
    print_puzzle(lines)
    
    lines = rotate_clockwise(lines)
    print_verbose("Puzzle after rotation:")
    print_puzzle(lines)
    
    result = solve(lines)

print(f"result: {result}")
```

## Part 2
```python
import numpy

VERBOSE = False
DEBUG = False

CYCLES = 1000000000
JUMP = True

def print_verbose(text):
    if VERBOSE:
        print(text)

def print_debug(text):
    if DEBUG:
        print(text)

def print_puzzle(lines):
    for line in lines:
        print_verbose(f"   {''.join(line)}")

def rotate_clockwise(lines):
    return list(zip(*lines[::-1]))

def move_rocks(lines):
    new_lines = []
    for line in lines:
        new_line = list(numpy.full(shape=len(line), fill_value='.'))
        fill_index = len(line)-1
        print_debug(f"Line before moving rocks: {line}")
        for i in range(len(line)-1, -1, -1):
            char = line[i]
            if(char == '#'):
                new_line[i] = '#'
                fill_index = i - 1
            elif(char == 'O'):
                new_line[fill_index] = 'O'
                fill_index -= 1
        print_debug(f"Line after moving rocks : {new_line}")
        new_lines.append(''.join(new_line))
    return new_lines

# Solve the puzzle, assuming the first line of "lines" is the northernmost side of the puzzle
def solve(lines):
    multiplier = len(lines)
    result = 0
    for line in lines:
        result += line.count('O') * multiplier
        multiplier -= 1

    return result

def cycle(lines):
    lines = rotate_clockwise(lines)
    lines = move_rocks(lines)
    return tuple(lines)

lines = []
cycle_of_puzzle = {}
key = None
with open('aoc14.txt', 'r') as file:
    for line in file:
        line = line.replace('\n', '')
        if(len(line) == 0):
            continue
        lines.append(line)

    print_verbose("Puzzle before rotation:")
    print_puzzle(lines)
    result = solve(tuple(lines))
    print_debug(f"Result is {result}");
    lines = tuple(lines)
    
    i = 0
    while(i < CYCLES):
        key = tuple(lines)

        for step in range(4): # A "cycle" is actually a whole rotation, so we need to do 4 steps
            lines = cycle(lines)

        if(cycle_of_puzzle.get(key) != None):
            diff = i - cycle_of_puzzle[key]
            remaining_cycles = CYCLES - i
            print_verbose(f"Found key {key} after cycling {i} times, as well as {cycle_of_puzzle[key]} times. Diff is {diff}.")
            jump = diff * (remaining_cycles // diff)
            print_debug(f"Jumping {jump} cycles")
            i += jump

        cycle_of_puzzle[key] = i
        i += 1
            

        result = solve(tuple(lines))
        print_debug(f"[{i}] Result is {result}");

print(f"result: {result}")
```