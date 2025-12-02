import re;

VERBOSE = False
DEBUG = False

def print_verbose(text):
    if VERBOSE:
        print(text)
        

def print_debug(text):
    if DEBUG:
        print(text)

with open('input.txt', 'r') as file:
    result = 0
    
    for line in file:
        tuples = re.findall(r'(\d+)-(\d+),?', line)
        for bounds in tuples:
            lowerBound = int(bounds[0])
            upperBound = int(bounds[1])
            print_debug(f"bounds: {lowerBound}..{upperBound}")
            
            for val in range(lowerBound, upperBound + 1):
                valStr = str(val)
                
                if re.match(r'^(\d+)\1+$', valStr):
                    print_debug(f"Value {val} matches regex")
                    result += int(val)

    print (f"result: {result}")
