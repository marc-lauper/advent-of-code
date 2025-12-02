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

                if len(valStr) % 2 == 0:

                    halfLength = len(valStr) // 2
                    firstHalf = valStr[0:halfLength]
                    secondHalf = valStr[halfLength:len(valStr)]
                    if firstHalf == secondHalf:
                        print_verbose(f"Found matching value: {val} (from bounds {lowerBound}..{upperBound})")
                        result += int(val)
                    elif val == 22:
                        print_debug(f"No match for value: {val} (from bounds {lowerBound}..{upperBound}). firstHalf: {firstHalf}, secondHalf: {secondHalf}")

    
    print (f"result: {result}")
