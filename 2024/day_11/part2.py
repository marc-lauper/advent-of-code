import re;
import os;
import datetime;
from functools import cache

VERBOSE = False
DEBUG = False

def print_verbose(text):
    if VERBOSE:
        print(text)

def print_debug(text):
    if DEBUG:
        print(text)

@cache
def get_next_stones(stone):
    new_list = []

    stone_as_str = str(stone)
    if stone == 0:
        new_list.append(1)
    elif len(stone_as_str) % 2 == 0:
        left_half = stone_as_str[:len(stone_as_str)//2]
        right_half = stone_as_str[len(stone_as_str)//2:]
        new_list.append(int(left_half))
        new_list.append(int(right_half))
    else:
        new_list.append(stone * 2024)

    return new_list

@cache
def blink_and_count(stone, times):
    print_verbose(f"[{stone}, {times}] Invoked")
    new_list = get_next_stones(stone)

    if times == 1:
        print_debug(f"[{stone}, {times}] {new_list}")
        return len(new_list)
    else:
        count = 0
        for i in range(len(new_list)-1, -1, -1):
            count += blink_and_count(new_list[i], times-1)
        return count
            

with open(os.path.dirname(os.path.abspath(__file__)) + '/input.txt', 'r') as file:
    result = 0
    starting_row = 0

    # Build a two-dimension array based on the content of the file
    for line in file:
        stones = re.findall(r'\d+', line)
        stones = list(map(int, stones))

    print_verbose(f"stones: {stones}")
    
    # go through the stones in reverse order
    # all_stones = []
    for i in range(len(stones)-1, -1, -1):
        progress_in_percent = (len(stones)-i)/len(stones)*100
        current_date_and_time = datetime.datetime.now()
        print(f"[{current_date_and_time}] Progress: {progress_in_percent:.2f}%")
        result += blink_and_count(stones[i], 75)

    print (f"\nresult: {result}")
