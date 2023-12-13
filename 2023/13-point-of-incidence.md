# Day 13 - Point of Incidence
See https://adventofcode.com/2023/day/13

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

def can_reflect_on_index(lines, reflection_point):
    for cursor in range(reflection_point):
        line_after = reflection_point + cursor
        line_before = reflection_point - cursor - 1
        if(line_before < 0 or line_after >= len(lines)):
            break
        if(lines[line_after] != lines[line_before]):
            return False
    return True

def solve_grid(lines, mirror_orientation):
    reflections = []
    r = 0
    
    for reflection_point in range(1, len(lines)):
        if(can_reflect_on_index(lines, reflection_point)):
            reflections.append(reflection_point)

    if(len(reflections) > 0):
        print_verbose(f"{mirror_orientation} reflection(s) found at row(s): {reflections}.")
        if(len(reflections) > 1):
            print_verbose(f"Multiple {mirror_orientation} reflections found. Combining them...")
        for reflection in reflections:
            r += reflection
    else:
        print_verbose(f"No {mirror_orientation} reflections found")

    return r

def solve_puzzle(lines):
    rotated_lines = []
    for line in lines:
        print_verbose(f"   {line}")
        for i in range(len(line)):
            if(i >= len(rotated_lines)):
                rotated_lines.append("")
            rotated_lines[i] += line[i]

    print_debug("LOOKING FOR VERTICAL REFLECTIONS")
    r = solve_grid(rotated_lines, "vertical")
    print_debug("LOOKING FOR HORIZONTAL  REFLECTIONS")
    r += 100 * solve_grid(lines, "horizontal")

    # Safety check
    if(r == 0):
        print("ERROR: No reflections found")
        exit()
    return r

result = 0
puzzle_number = 0
lines = []
with open('aoc13.txt', 'r') as file:
    print_verbose(f"PROCESSING PUZZLE NUMBER {puzzle_number}")
    for line in file:
        line = line.replace('\n', '')
        if(len(line) == 0):
            # Solve the current puzzle
            result += solve_puzzle(lines)

            # Prepare next puzzle
            puzzle_number += 1
            print_verbose(f"\nPROCESSING PUZZLE NUMBER {puzzle_number}")
            lines = []
            continue

        print_debug("Processing line " + line)
        lines.append(line)

if(len(lines) > 0):
    # Prepare next puzzle
    result += solve_puzzle(lines)
        
print("result: " + str(result) + " solutions found")
```
