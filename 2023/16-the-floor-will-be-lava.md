# Day 16 - The Floor Will Be Lava
See https://adventofcode.com/2023/day/16

## Part 1
```python
import sys

sys.setrecursionlimit(10**6)

VERBOSE = False

class Cell:
    def __init__(self):
        self.symbol = '.'
        self.energized = 0
        # Avoid infinite loops, etc.
        self.walked_from = []

def print_verbose(text):
    if VERBOSE:
        print(text)

def print_puzzle(lines):
    if not VERBOSE:
        return
    for line in lines:
        for cell in line:
            if(cell.energized > 0):
                print(cell.energized, end='')
            else:
                print(cell.symbol, end='')
        print()

def energize(data, current_x, current_y, direction):
    
    # Move our position depending of the current position and direction
    if(direction == 'R'):
        current_x += 1
        if(current_x >= len(data[current_y])):
            return
    elif(direction == 'L'):
        current_x -= 1
        if(current_x < 0):
            return
    elif(direction == 'U'):
        current_y -= 1
        if(current_y < 0):
            return
    elif(direction == 'D'):
        current_y += 1
        if(current_y >= len(data)):
            return

    # Avoid infinite loops
    if(direction in data[current_y][current_x].walked_from):
        return
    data[current_y][current_x].walked_from.append(direction)

    print_verbose("\n")
    print_puzzle(data)
    print_verbose(f"Processing cell ({current_x}, {current_y})")

    data[current_y][current_x].energized += 1

    # Switch the direction epending of the symbol:
    symbol = data[current_y][current_x].symbol
    if(symbol == '\\'):
        if(direction == 'R'):
            direction = 'D'
        elif(direction == 'L'):
            direction = 'U'
        elif(direction == 'U'):
            direction = 'L'
        elif(direction == 'D'):
            direction = 'R'
    elif(symbol == '/'):
        if(direction == 'R'):
            direction = 'U'
        elif(direction == 'L'):
            direction = 'D'
        elif(direction == 'U'):
            direction = 'R'
        elif(direction == 'D'):
            direction = 'L'
    elif(symbol == '|' and (direction == 'L' or direction == 'R')):
        energize(data, current_x, current_y, 'U')
        energize(data, current_x, current_y, 'D')
        return
    elif(symbol == '-' and (direction == 'U' or direction == 'D')):
        energize(data, current_x, current_y, 'L')
        energize(data, current_x, current_y, 'R')
        return

    energize(data, current_x, current_y, direction)

def count_energized(data):
    count = 0
    for row in data:
        for cell in row:
            if(cell.energized > 0):
                count += 1
    return count

data = []
with open('aoc16.txt', 'r') as file:
    for line in file:
        # For eveyr character on the line, create a new Cell objec whose value is the character
        row = []
        for character in line:
            if(character == '\n'):
                continue
            cell = Cell()
            cell.symbol = character
            row.append(cell)
        data.append(row)

energize(data, -1, 0, 'R')

print(f"Result: {count_energized(data)}")
```

## Part 2
It's dirty but it works fast enough.
```python
import sys

sys.setrecursionlimit(10**6)

VERBOSE = False

class Cell:
    def __init__(self):
        self.symbol = '.'
        self.energized = 0
        # Avoid infinite loops, etc.
        self.walked_from = []

def print_verbose(text):
    if VERBOSE:
        print(text)

def print_puzzle(lines):
    if not VERBOSE:
        return
    for line in lines:
        for cell in line:
            if(cell.energized > 0):
                print(cell.energized, end='')
            else:
                print(cell.symbol, end='')
        print()

def energize(data, current_x, current_y, direction):
    
    # Move our position depending of the current position and direction
    if(direction == 'R'):
        current_x += 1
        if(current_x >= len(data[current_y])):
            return
    elif(direction == 'L'):
        current_x -= 1
        if(current_x < 0):
            return
    elif(direction == 'U'):
        current_y -= 1
        if(current_y < 0):
            return
    elif(direction == 'D'):
        current_y += 1
        if(current_y >= len(data)):
            return

    # Avoid infinite loops
    if(direction in data[current_y][current_x].walked_from):
        return
    data[current_y][current_x].walked_from.append(direction)

    print_verbose("\n")
    print_puzzle(data)
    print_verbose(f"Processing cell ({current_x}, {current_y})")

    data[current_y][current_x].energized += 1

    # Switch the direction epending of the symbol:
    symbol = data[current_y][current_x].symbol
    if(symbol == '\\'):
        if(direction == 'R'):
            direction = 'D'
        elif(direction == 'L'):
            direction = 'U'
        elif(direction == 'U'):
            direction = 'L'
        elif(direction == 'D'):
            direction = 'R'
    elif(symbol == '/'):
        if(direction == 'R'):
            direction = 'U'
        elif(direction == 'L'):
            direction = 'D'
        elif(direction == 'U'):
            direction = 'R'
        elif(direction == 'D'):
            direction = 'L'
    elif(symbol == '|' and (direction == 'L' or direction == 'R')):
        energize(data, current_x, current_y, 'U')
        energize(data, current_x, current_y, 'D')
        return
    elif(symbol == '-' and (direction == 'U' or direction == 'D')):
        energize(data, current_x, current_y, 'L')
        energize(data, current_x, current_y, 'R')
        return

    energize(data, current_x, current_y, direction)

def count_energized(data):
    count = 0
    for row in data:
        for cell in row:
            if(cell.energized > 0):
                count += 1
    return count

def reset(data):
    for row in data:
        for cell in row:
            cell.energized = 0
            cell.walked_from = []

data = []
with open('aoc16.txt', 'r') as file:
    for line in file:
        # For eveyr character on the line, create a new Cell objec whose value is the character
        row = []
        for character in line:
            if(character == '\n'):
                continue
            cell = Cell()
            cell.symbol = character
            row.append(cell)
        data.append(row)

result = 0
possibilities = len(data)*2 + len(data[0])*2
i = 0

for y in range(len(data)):
    print(f"processing possibility {i} of {possibilities}")
    i += 1
    energize(data, -1, y, 'R')
    r = count_energized(data)
    if(r > result):
        result = r
    reset(data)

    print(f"processing possibility {i} of {possibilities}")
    i += 1
    energize(data, len(data[0]), y, 'L')
    r = count_energized(data)
    if(r > result):
        result = r
    reset(data)
    
for x in range(len(data[0])):
    print(f"processing possibility {i} of {possibilities}")
    i += 1
    energize(data, x, -1, 'D')
    r = count_energized(data)
    if(r > result):
        result = r

    print(f"processing possibility {i} of {possibilities}")
    i += 1
    reset(data)
    energize(data, x, len(data), 'U')
    r = count_energized(data)
    if(r > result):
        result = r
    reset(data)

print(f"Result: {result}")
```