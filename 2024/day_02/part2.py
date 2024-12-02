import re;

VERBOSE = False
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
            print_verbose(f"  [error] {report} --> {current_report} == {next_report}")
            return False
        if abs(current_report - next_report) > 3:
            print_verbose(f"  [error] {report} --> {current_report} - {next_report}  = {abs(current_report - next_report)} > 3")
            return False
        if current_report < next_report:
            increasing = True
        else:
            decreasing = True
        if not increasing ^ decreasing:
            print_verbose(f"  [error] {report} --> Changed direction at {i}")
            return False
    print_verbose(f"  [safe] {report}")
    return True

def is_safely_dampened(report):
    if is_safe(report):
        return True
    for i in range(len(report)):
        new_report = report[:i] + report[i+1:]
        if is_safe(new_report):
            print_verbose(f"[made safe by removing element {i}] {report} -> {new_report}")
            return True
    print_verbose(f"[could not be made safe] {report}")
    return False

with open('input.txt', 'r') as file:
    result = 0
    
    for report in file:
        levels = re.findall(r'(\d+)', report)
        if(len(levels) < 3):
            print_debug(f"short levels: {levels}")
        if(is_safely_dampened(levels)):
            result += 1
    
    print (f"result: {result}")
