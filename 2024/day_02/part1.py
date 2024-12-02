import re;

VERBOSE = True
DEBUG = False

def print_verbose(text):
    if VERBOSE:
        print(text)
        

def print_debug(text):
    if DEBUG:
        print(text)

def is_safe(report):
    increasing = False
    decreasing = False
    for i in range(len(report)-1):
        current_report = int(report[i])
        next_report = int(report[i+1])
        if current_report == next_report:
            return False
        if abs(current_report - next_report) > 3:
            return False
        if current_report < next_report:
            increasing = True
        else:
            decreasing = True
        if not increasing ^ decreasing:
            return False
    return True

with open('input.txt', 'r') as file:
    result = 0
    
    for report in file:
        levels = re.findall(r'(\d+)', report)
        print_debug(f"levels: {levels}")
        if(is_safe(levels)):
            result += 1
    
    print (f"result: {result}")
