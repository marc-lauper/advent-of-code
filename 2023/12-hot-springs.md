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
Still working on it. Can't just loop over part 1, that would literally take ages...