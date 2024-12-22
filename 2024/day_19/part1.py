import re, sys, os;
sys.setrecursionlimit(10**6)

VERBOSE = True
DEBUG = True
FILE = "input.txt"
available = []
desired_patterns = []
cache = set()

def print_verbose(text):
    if VERBOSE:
        print(text)

def print_debug(text):
    if DEBUG:
        print(text)

def can_build_desired_pattern(desired, subpattern = ""):
    global cache
    
    if (subpattern == ""):
        cache = set()

    if(len(subpattern) > 0):
        if subpattern in cache:
            return False
        else:
            cache.add(subpattern)
        
    if desired in cache:
        return True
    
    if len(subpattern) > len(desired):
        return False
   
    if(subpattern != desired[:len(subpattern)]):
        return False
    
    if(len(subpattern) == len(desired)):
        return subpattern == desired

    for available_item in available:
        if can_build_desired_pattern(desired, subpattern + available_item):
            return True

    print(f"{subpattern} != {desired}") #, end="\r")
    return False

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
        if can_build_desired_pattern(d):
            print_verbose(f"[OK] {d}")
            result += 1
        else:
            print_verbose(f"[FAIL] {d}")
        print()

    print (f"\nresult: {result}")
