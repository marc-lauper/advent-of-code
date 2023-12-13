# Day 13 - Point of Incidence
See https://adventofcode.com/2023/day/13

```python
VERBOSE = False
DEBUG = False

def print_verbose(text):
    if VERBOSE:
        print(text)
        

def print_debug(text):
    if DEBUG:
        print(text)

def diff_between_lines(line1, line2):
    diff = 0
    for i in range(len(line1)):
        if(line1[i] != line2[i]):
            diff += 1
    return diff

def can_reflect_on_index(lines, reflection_point, smudge):
    diff = 0
    for cursor in range(reflection_point):
        line_after = reflection_point + cursor
        line_before = reflection_point - cursor - 1
        if(line_before < 0 or line_after >= len(lines)):
            break
        diff += diff_between_lines(lines[line_after], lines[line_before])
        if(diff > smudge):
            return False
    return diff == smudge

def solve_grid(lines, mirror_orientation, smudge):
    reflections = []
    r = 0
    
    for reflection_point in range(1, len(lines)):
        if(can_reflect_on_index(lines, reflection_point, smudge)):
            reflections.append(reflection_point)

    if(len(reflections) > 0):
        print_verbose(f"{mirror_orientation} reflection(s) found at row(s): {reflections}.")
        for reflection in reflections:
            r += reflection
    else:
        print_verbose(f"No {mirror_orientation} reflections found")

    return r

def solve_puzzle(lines, smudge):
    rotated_lines = []
    for line in lines:
        print_verbose(f"   {line}")
        for i in range(len(line)):
            if(i >= len(rotated_lines)):
                rotated_lines.append("")
            rotated_lines[i] += line[i]

    print_debug("LOOKING FOR VERTICAL REFLECTIONS")
    r = solve_grid(rotated_lines, "vertical", smudge)
    print_debug("LOOKING FOR HORIZONTAL  REFLECTIONS")
    r += 100 * solve_grid(lines, "horizontal", smudge)

    # Safety check
    if(r == 0):
        print("ERROR: No reflections found")
        exit()
    return r

result1 = 0
result2 = 0
puzzle_number = 0
lines = []
with open('aoc13.txt', 'r') as file:
    print_verbose(f"PROCESSING PUZZLE NUMBER {puzzle_number}")
    for line in file:
        line = line.replace('\n', '')
        if(len(line) == 0):
            # Solve the current puzzle
            result1 += solve_puzzle(lines, 0)
            result2 += solve_puzzle(lines, 1)

            # Prepare next puzzle
            puzzle_number += 1
            print_verbose(f"\nPROCESSING PUZZLE NUMBER {puzzle_number}")
            lines = []
            continue

        print_debug("Processing line " + line)
        lines.append(line)

if(len(lines) > 0):
    # Solve the last puzzle
    result1 += solve_puzzle(lines, 0)
    result2 += solve_puzzle(lines, 1)
        
print("result1: " + str(result1) + " solutions found")
print("result2: " + str(result2) + " solutions found")
```
