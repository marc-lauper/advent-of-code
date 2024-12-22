import re, sys, os;
from functools import cache

sys.setrecursionlimit(10**6)

VERBOSE = True
DEBUG = True
FILE = "input.txt"
available = []
desired_patterns = []
failures = set()

def print_verbose(text):
    if VERBOSE:
        print(text)

def print_debug(text):
    if DEBUG:
        print(text)

@cache
def can_build_desired_pattern(desired, subpattern = ""):
    global failures
    result = 0
    
    if (subpattern == ""):
        failures = set()

    if(len(subpattern) > 0):
        if subpattern in failures:
            return 0
        else:
            failures.add(subpattern)
        
    if desired == subpattern:
        return 1
    
    if len(subpattern) > len(desired):
        return 0
   
    if(subpattern != desired[:len(subpattern)]):
        return 0
    
    if(len(subpattern) == len(desired)):
        return subpattern == desired

    for available_item in available:
        result += can_build_desired_pattern(desired, subpattern + available_item)
    return result

with open(os.path.dirname(os.path.abspath(__file__)) + '/' + FILE, 'r') as file:
    result = 0

    for line in file:
        line = line.replace('\n', '')
        if len(line) == 0:
            continue

        match = re.match(r"^(\w+)$", line)
        if match:
            desired_patterns.append(match.group(1))
            continue
        
        match = re.findall(r"(\w+)", line)
        if match:
            available = match

    print_debug(f"available: {available}")
    print_debug(f"desired: {desired_patterns}")

    for d in desired_patterns:
        result += can_build_desired_pattern(d)

    print (f"\nresult: {result}")
