# Day 12 - Hot Springs
See https://adventofcode.com/2023/day/12

## Part 1
```python
import re

VERBOSE = False

OPERATIONAL = '0'
DAMAGED = '1'
UNKNOWN = 'x'

def print_verbose(text):
    if VERBOSE:
        print(text)

def find_solutions(springs, regex):
    
    result = 0
    if(UNKNOWN in springs):
        result += find_solutions(springs.replace(UNKNOWN, OPERATIONAL, 1), regex)
        result += find_solutions(springs.replace(UNKNOWN, DAMAGED, 1), regex)
        return result
    else:
        if re.match(regex, springs):
            print_verbose("Found match: " + springs)
            return 1
        else:
            return 0

result = 0
with open('aoc12.txt', 'r') as file:
    for line in file:
        # Replacing symbols because dots and question marks tends to be a mess in regexes...
        line = line.replace('.', '0')
        line = line.replace('#', '1')
        line = line.replace('?', 'x')
        line = line.replace('\n', '')
        print ("Processing line " + line)
        line = line.split(' ')
        springs = line[0]
        damaged_springs_checksums = list(map(int,line[1].split(',')))
        
        regex = r"^"
        first = True
        for checksum in damaged_springs_checksums:
            regex += OPERATIONAL
            if first:
                regex += r"*"
                first = False
            else:
                regex += r"+"
            regex += DAMAGED + r"{" + str(checksum) + r"}"
        regex += OPERATIONAL + r"*$"
        print_verbose("Regex: " + regex)
        
        to_add = find_solutions(springs, re.compile(regex))
        print("Found " + str(to_add) + " solutions")
        result += to_add
        print("")
        
print("result: " + str(result) + " solutions found")
```

## Part 2
```python
from functools import cache

INCREASE = 5

OPERATIONAL = '.'
DAMAGED = '#'
UNKNOWN = '?'

@cache
def find_solutions(springs, checksums, damaged_count = 0):
    
    # End of the recursion when there are no more springs to inspect...
    if(len(springs) == 0):
        checksum_length = len(checksums)
        if(checksum_length == 0):
            return 1 if damaged_count == 0 else 0
        elif(checksum_length == 1):
            return 1 if damaged_count == checksums[0] else 0
        else:
            return 0
    
    spring = springs[0]
    new_springs = springs[1:]
    
    if(spring == UNKNOWN):
        return find_solutions('#' + new_springs, checksums, damaged_count) + find_solutions('.' + new_springs, checksums, damaged_count)

    checksum = 0 if len(checksums) == 0 else checksums[0]

    if(damaged_count > checksum):
        return 0
    
    if(spring == DAMAGED):
        return find_solutions(new_springs, checksums, damaged_count + 1)

    if(spring == OPERATIONAL):
        if(damaged_count == 0):
            return find_solutions(new_springs, checksums, 0)
        elif(damaged_count == checksum):
            return find_solutions(new_springs, checksums[1:], 0)
        else:
            return 0

result = 0
with open('aoc12.txt', 'r') as file:
    for line in file:
        line = line.replace('\n', '')
        print ("Processing line " + line)
        line = line.split(' ')
        springs = line[0]
        checksums = line[1]
        for i in range(INCREASE-1):
            springs += UNKNOWN + line[0]
            checksums += "," + line[1]
        damaged_springs_checksums = tuple(map(int,checksums.split(',')))
        
        to_add = find_solutions(springs, damaged_springs_checksums)
        print("Found " + str(to_add) + " solutions")
        result += to_add
        print("")
        
print("result: " + str(result) + " solutions found")

```